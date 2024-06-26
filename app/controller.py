import secrets
from passlib.hash import pbkdf2_sha256
from fastapi.responses import JSONResponse

from .model import connect
from fastapi import HTTPException
from dotenv import dotenv_values
from auth.auth_handler import sign_jwt
import re

config = dotenv_values('.env')

SECRET_KEY = config['SECRET_KEY']


def check_if_username_exists(username):
    exists = False

    conn = connect()
    cursor = conn.cursor()

    cursor.execute('SELECT username FROM users WHERE username = %s;', (username,))
    result = cursor.fetchone()

    if result is not None:
        exists = True

    conn.commit()

    cursor.close()
    conn.close()

    return exists


def check_if_field_is_alphanumeric(field):
    return re.match('^[A-Za-z0-9]+$', field)


def check_if_field_is_alphabetical(field):
    return re.match('^[A-Za-z]+$', field)


def register_user(username, password, first_name, last_name, is_admin=False, is_enabled=True, test=False):
    if username is None or password is None or first_name is None or last_name is None:
        raise HTTPException(status_code=400, detail='Missing required field')

    if len(username) < 3 or len(username) > 20:
        raise HTTPException(status_code=400, detail='Username must be between 3 and 20 characters')

    if check_if_username_exists(username):
        raise HTTPException(status_code=400, detail='Username already exists')

    if not check_if_field_is_alphanumeric(username):
        raise HTTPException(status_code=400, detail='Username should only contain alphanumeric characters')

    if not check_if_field_is_alphabetical(first_name):
        raise HTTPException(status_code=400, detail='First name should only contain alphabetical characters')

    if not check_if_field_is_alphabetical(last_name):
        raise HTTPException(status_code=400, detail='Last name should only contain alphabetical characters')

    if len(password) < 8:
        raise HTTPException(status_code=400, detail='Password must be at least 8 characters')

    has_capital = False
    has_lowercase = False
    has_number = False
    has_special = False
    for ch in range(0, len(password)):
        if password[ch] in 'QWERTYUIOPASDFGHJKLZXCVBNM':
            has_capital = True

        if password[ch] in 'qwertyuiopasdfghjklzxcvbnm':
            has_lowercase = True

        if password[ch] in '1234567890':
            has_number = True

        if password[ch] in '`~!@#$%^&*()_-+=|\\]}[{\'";:/?.>,<':
            has_special = True

    if not has_capital:
        raise HTTPException(status_code=400, detail='Password must contain at least 1 capital letter')

    if not has_lowercase:
        raise HTTPException(status_code=400, detail='Password must contain at least 1 lowercase letter')

    if not has_number:
        raise HTTPException(status_code=400, detail='Password must contain at least 1 number')

    if not has_special:
        raise HTTPException(status_code=400, detail='Password must contain at least 1 special character')

    salt = secrets.token_urlsafe(8)
    hashed_password = pbkdf2_sha256.hash(str.join(password, salt))

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO users(username, password_digest, password_salt, first_name, last_name, is_admin, is_enabled) VALUES (%s, %s, %s, %s, %s, %s, %s);',
        (username, hashed_password, salt, first_name, last_name, is_admin, is_enabled))

    conn.commit()

    cursor.close()
    conn.close()

    return {'username': username, 'first_name': first_name, 'last_name': last_name}


def login_user(username, password):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = %s;', (username,))
    result = cursor.fetchone()

    if not result:
        raise HTTPException(status_code=401, detail='Invalid username/password combination')

    is_admin = result[6]
    hashed_password = result[2]
    salt = result[3]
    is_enabled = result[7]

    cursor.close()
    conn.close()

    if not is_enabled:
        raise HTTPException(status_code=401, detail='User account is disabled')

    if pbkdf2_sha256.verify(str.join(password, salt), hashed_password):
        signed_jwt = sign_jwt(username, hashed_password, is_admin)

        response = JSONResponse(content={'token': signed_jwt, 'token_type': 'Bearer'})
        response.set_cookie(key='token', value=signed_jwt['token'], httponly=True)

        return response
    else:
        raise HTTPException(status_code=401, detail='Invalid login attempt')


def logout_user():
    response = JSONResponse(content={'message': 'Logged out successfully'})
    response.set_cookie(key='token', value='', httponly=True)

    return response


def list_all_users():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users ORDER BY id;')
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


def get_user_by_user_id(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = %s;', (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


def update_user_by_id(user_id, username, first_name, last_name, is_admin, is_enabled):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('UPDATE users SET username = %s, first_name = %s, last_name = %s, is_admin = %s, is_enabled = %s WHERE id = %s;',
                   (username, first_name, last_name, is_admin, is_enabled, user_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        username: username,
        first_name: first_name,
        last_name: last_name,
        is_admin: is_admin,
    }


def delete_user_by_id(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM users WHERE id = %s;', (user_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return {'message': f'User with ID: {user_id} deleted'}
