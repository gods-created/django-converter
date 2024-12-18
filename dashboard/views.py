from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import (
    APIView,
)
from .serializers import (
    SignUpTokenSerializer,
)
from .models import (
    User as UserModel
)
from .minions import (
    generate_token,
    generate_task,
)
from .forms import (
    Converter as ConverterForm,
    Quiz as QuizForm
)
from copy import deepcopy
from typing import Any

class Base(APIView):
    def __init__(self):
        super().__init__()
        self.response_json = {
            'status': 'error',
            'err_description': ''
        }
    
    def _get_session_token(self, request):
        return request.COOKIES.get('session_token', '')

class Dashboard(Base):
    def get(self, request, format=None) -> Any:
        try:
            session_token = self._get_session_token(request)
            if not session_token:
                session_token = generate_token()
                serializer = SignUpTokenSerializer(data={'session_token': session_token})
                if not serializer.is_valid():
                    errors = serializer.errors.items()
                    for error in errors:
                        message, *_ = [str(err) for err in error[1]]
                        raise ValueError(
                            message
                        )

                serializer.save()

            user = UserModel.objects.using('users').filter(session_token=session_token).values('attempts__count').first() or {}
            
            converter_form = ConverterForm()
            quiz_form = QuizForm()
            task_response, task_string = generate_task()

            response = render(request=request, template_name='dashboard/base.html', context={
                'user': user,
                'converter_form': converter_form,
                'quiz_form': quiz_form,
                'task_string': task_string,
            })

            response.set_cookie('task_response', task_response)
            response.set_cookie('session_token', session_token)
            return response
        
        except (ValueError, Exception, ) as e:
            return HttpResponse(str(e))