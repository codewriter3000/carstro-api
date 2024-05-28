import secrets
import sys
from passlib.hash import pbkdf2_sha256
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


def register_user(username, password, first_name, last_name, is_admin=False, test=False):
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

    if test:
        print(f'Hashed password: {hashed_password}')

        # Expecting True
        print(pbkdf2_sha256.verify(str.join(password, salt), hashed_password))

        # Expecting False
        print(pbkdf2_sha256.verify(password, hashed_password))
        print(pbkdf2_sha256.verify(str.join('P@ss', salt), hashed_password))
    
    else:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO users(username, password_digest, password_salt, first_name, last_name, is_admin) VALUES (%s, %s, %s, %s, %s, %s);', (username, hashed_password, salt, first_name, last_name, is_admin))

        conn.commit()

        cursor.close()
        conn.close()

    return {'username': username, 'first_name': first_name, 'last_name': last_name}


def login_user(username, password):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = %s;', (username,))
    result = cursor.fetchone()

    is_admin = result[6]
    hashed_password = result[2]
    salt = result[3]

    cursor.close()
    conn.close()

    if pbkdf2_sha256.verify(str.join(password, salt), hashed_password):
        return sign_jwt(username, hashed_password, is_admin)
    else:
        raise HTTPException(status_code=401, detail='Invalid login attempt')


def list_all_users():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users;')
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


async def update_user(user_id, user_data):
    conn = connect()
    cursor = conn.cursor()

    await cursor.execute('UPDATE users SET username = %s, first_name = %s, last_name = %s WHERE id = %s;',
                   (user_data['username'], user_data['first_name'], user_data['last_name'], user_id,))

    cursor.close()
    conn.close()

    return user_data


def delete_user(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM users WHERE user_id = %s', (user_id,))

    cursor.close()
    conn.close()

    return {'message': f'User with ID: {user_id} deleted'}


if __name__ == '__main__':
    if sys.argv[1] == 'register_user':
        register_user('test_user', 'P@ssword123', 'Test', 'User', test=True)
