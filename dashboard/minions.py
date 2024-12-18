from random import choice, choices
from string import ascii_letters, digits
from cryptography.fernet import Fernet
from django.forms import Form
from dashboard.models import (
    User as UserModel,
    Attempts as AttemptsModel
)
import aiohttp
import asyncio

async def currency_data_feed_api(from_: str, value_: int, to_: str) -> dict:
    response_json = {
        'status': 'error',
        'err_description': '',
        'value': 0
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://economia.awesomeapi.com.br/{from_}-{to_}') as request:
                request.raise_for_status()
                response = await request.json()

        if len(response) == 0:
            raise Exception(
                'Something went wrong. Try again'
            )

        ask_ = response[0].get('ask', 1)

        try:
            value_ = float(value_)
            ask_ = float(ask_)
        except ValueError:
            raise Exception('Incorrect value type. Value must be a numeric string.')

        response_json['status'] = 'success'
        response_json['value'] = value_ * ask_

    except (Exception, ) as e:
        response_json['err_description'] = str(e)

    finally:
        return response_json
 
def start_convert(session_token: str, form: Form) -> str:
    user = UserModel.objects.using('users').filter(session_token=session_token).values('attempts__id', 'attempts__count').first()
    if not user:
        return 'Error! You as user not found'
    
    attempts__id, attempts__count = user.get('attempts__id'), user.get('attempts__count')

    if attempts__count == 0:
        return 'You havn\'t attempts to converting. Decide issue from quiz'

    from_, value_, to_ = form.cleaned_data['from_'], form.cleaned_data['value_'], form.cleaned_data['to_']
    currency_data_feed_api_response = asyncio.run(
        currency_data_feed_api(from_, value_, to_)
    )
    print(currency_data_feed_api_response)

    if currency_data_feed_api_response.get('status', 'error') == 'error':
        return currency_data_feed_api_response.get('err_description', 'Error! API not working now')

    value_ = currency_data_feed_api_response.get('value', 0.00)

    AttemptsModel.objects.using('users').filter(id=attempts__id).update(
        count = attempts__count - 1
    )
    
    return f'{value_:.2f} {to_}'

def get_cookies(request) -> tuple:
    return (
        request.COOKIES.get('session_token', ''),
        request.COOKIES.get('task_response', ''),
    )

def check_task_response(session_token: str, task_response: str, form: Form) -> str:
    user_response = form.cleaned_data['response']
    if task_response != user_response:
        return 'Incorrect response'

    user = UserModel.objects.using('users').filter(session_token=session_token).values('attempts__id', 'attempts__count').first()
    if not user:
        return 'Error! You as user not found'
    
    attempts__id, attempts__count = user.get('attempts__id'), user.get('attempts__count')
    AttemptsModel.objects.using('users').filter(id=attempts__id).update(
        count = attempts__count + 1
    )

    return 'Success! You got one attempt for using converter'

def generate_token() -> str:
    body = ''.join(choice(ascii_letters + digits) for _ in range(50))
    key = Fernet.generate_key()
    f = Fernet(key)
    return f.encrypt(body.encode()).decode()

def generate_task() -> tuple:
    first_number = choice(range(1, 100))
    second_number = choice(range(1, 100))
    symbol = choice(['/', '*', '+', '-'])
    
    if symbol == '+':
        task_response = first_number + second_number
    elif symbol == '-':
        task_response = first_number - second_number
    elif symbol == '*':
        task_response = first_number * second_number
    elif symbol == '/':
        task_response = round(first_number / second_number, 2)

    task_string = f'{first_number} {symbol} {second_number} = ?'

    return (
        task_response,
        task_string
    )