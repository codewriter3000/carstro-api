import time

import jwt
from dotenv import dotenv_values
from fastapi.encoders import jsonable_encoder

config = dotenv_values('.env')
SECRET_KEY = config['SECRET_KEY']


def sign_jwt(username, password):
    data = jsonable_encoder({'username': username, 'password': password, 'expires': time.time() + 600})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm='HS256')

    return {
        'token': encoded_jwt,
    }


def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return {}
