from django.urls import path
from .views import (
    convert,
    quiz,
)

urlpatterns = [
    path('convert', convert, name='Convert'),
    path('quiz', quiz, name='Quiz'),
]