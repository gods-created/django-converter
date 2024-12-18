from django.forms import (
    Form,
    CharField,
    ChoiceField,
    IntegerField,
    NumberInput,
    TextInput,
    Select
)
from enum import Enum

class Currencies(Enum):
    USD = 'USD'
    EUR = 'EUR'
    UAH = 'UAH'

class Quiz(Form):
    response = CharField(
        min_length=1,
        max_length=300,
        required=True,
        widget=TextInput(
            attrs={'class': 'form-control mb-3'}
        ),
        error_messages = {
            'min_length': 'The response have to have min. 1 character',
            'max_length': 'The response have to have max. 300 characters',
            'required': 'The response is required'
        }
    )

class Converter(Form):
    from_ = ChoiceField(
        label='From',
        widget=Select(
            attrs={'class': 'form-select mb-3'}
        ),
        choices=(
            (v.value, v.value) for v in Currencies
        ),
        required=True,
        error_messages={
            'required': 'This field \'From\' is requried'
        },
    )

    value_ = IntegerField(
        label='Value',
        widget=NumberInput(
            attrs={'class': 'form-control mb-3'}
        ),
        min_value=1,
        required=True,
        error_messages={
            'required': 'This field \'Value\' is requried',
            'min_value': 'Min. value is 1'
        },
    )

    to_ = ChoiceField(
        label='To',
        widget=Select(
            attrs={'class': 'form-select mb-3'}
        ),
        choices=(
            (v.value, v.value) for v in Currencies
        ),
        required=True,
        error_messages={
            'required': 'This field \'To\' is requried'
        },
    )