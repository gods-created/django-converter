from django.db.models import (
    Model,
    CharField,
    DateTimeField,
    IntegerField,
    ManyToManyField,
)

class User(Model):
    session_token = CharField(
        max_length=200,
        null=False,
        unique=True,
        error_messages={
            'max_length': 'Max session token length is 200 characters',
            'null': 'Session token can\'t to be empty',
            'unique': 'This token is already existing'
        }
    )

    created_at = DateTimeField(
        auto_now_add=True
    )

    class Meta:
        app_label = 'dashboard'
        db_table = 'users'
        ordering = ['id', 'session_token']
    
    def __str__(self):
        return self.session_token

class Attempts(Model):
    users = ManyToManyField(User)

    count = IntegerField(
        null=False,
        default=0,
        error_messages={
            'null': 'Attempt count can\'t to be empty',
        }
    )

    class Meta:
        app_label = 'dashboard'
        db_table = 'attempts'
        ordering = ['id', 'count']

    def __str__(self):
        return self.count
    