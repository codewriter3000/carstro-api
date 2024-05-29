import time

import jwt
from dotenv import dotenv_values
from fastapi.encoders import jsonable_encoder

config = dotenv_values('.env')
SECRET_KEY = config['SECRET_KEY']


def sign_jwt(username, password, is_admin):
    expiration = time.time() + 600

    data = jsonable_encoder({'username': username, 'password': password,
                             'expiration': expiration, 'is_admin': is_admin})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm='HS256')

    return {
        'token': encoded_jwt,
        'expiration': expiration,
    }


def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return {}


def decode_jwt_admin(token):
    try:
        print(token)
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(decoded_token['is_admin'])
        return decoded_token if decoded_token['expires'] >= time.time() and decoded_token['is_admin'] else None
    except:
        print('exception')
        return {}
