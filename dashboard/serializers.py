from rest_framework.serializers import (
    Serializer,
    ValidationError,
    CharField
)
from .models import (
    User as UserModel,
    Attempts as AttemptsModel
)

class SignUpTokenSerializer(Serializer):
    session_token = CharField(
        max_length=200,
        min_length=1,
        required=True,
        error_messages={
            'max_length': 'Max session token length is 200 characters',
            'min_length': 'Min session token length is 1 character',
            'required': 'Session token is required'
        }
    )

    def create(self, validated_data):
        user, *_ = UserModel.objects.using('users').get_or_create(**validated_data)
        attempts = AttemptsModel.objects.using('users').create(count=0)
        attempts.users.add(user)

        return user