import time

import jwt
from dotenv import dotenv_values
from fastapi.encoders import jsonable_encoder

config = dotenv_values('.env')
SECRET_KEY = config['SECRET_KEY']


def sign_jwt(username, password, is_admin):
    expiration = time.time() + 86400

    data = jsonable_encoder({'username': username, 'password': password,
                             'expiration': expiration, 'is_admin': is_admin})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm='HS256')

    return {
        'token': encoded_jwt,
        'expiration': expiration,
    }


def decode_jwt(token):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return decoded_token if decoded_token['expires'] >= time.time() else None


def decode_jwt_admin(token):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    if decoded_token['expiration'] <= time.time():
        return {'is_valid': False, 'message': 'Session expired'}

    if decoded_token['is_admin']:
        decoded_token['is_valid'] = True
        return decoded_token
    else:
        print('not admin')
        return {'is_valid': False,
                'message': 'This is for administrators only'}
