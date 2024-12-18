from django.http import HttpResponseRedirect
from typing import Any
from dashboard.minions import (
    check_task_response,
    get_cookies,
    start_convert,
)
from dashboard.forms import (
    Converter, 
    Quiz,
)

def convert(request) -> Any:
    message = ''

    try:
        method = request.method
        if method != 'POST':
            raise Exception(
                f'Method \'{method}\' not allowed'
            )

        form = Converter(request.POST)
        if not form.is_valid():
            errors = form.errors.items()
            for error in errors:
                message, *_ = [str(err) for err in error[1]]
                raise Exception(
                    message
                )
        
        session_token, *_ = get_cookies(request)
        message = start_convert(session_token, form)

    except (Exception, ) as e:
        message = str(e)

    finally:
        response = HttpResponseRedirect(
            '/dashboard/'
        )
        response.set_cookie(
            'answer', message
        )

        return response

def quiz(request) -> Any:
    message = ''

    try:
        method = request.method
        if method != 'POST':
            raise Exception(
                f'Method \'{method}\' not allowed'
            )

        form = Quiz(request.POST)
        if not form.is_valid():
            errors = form.errors.items()
            for error in errors:
                message, *_ = [str(err) for err in error[1]]
                raise Exception(
                    message
                )
        
        session_token, task_response = get_cookies(request)
        message = check_task_response(
            session_token, task_response, form
        )

    except (Exception, ) as e:
        message = str(e)

    finally:
        response = HttpResponseRedirect(
            '/dashboard/'
        )
        response.set_cookie(
            'answer', message
        )

        return response
