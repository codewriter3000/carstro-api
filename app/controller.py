from passlib.hash import pbkdf2_sha256
from .model import connect
from fastapi import HTTPException

import secrets
import sys
import base64


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


def register_user(username, password, first_name, last_name, test=False):
    if username is None or password is None or first_name is None or last_name is None:
        raise HTTPException(status_code=400, detail='Missing required field')

    if len(username) < 3 or len(username) > 20:
        raise HTTPException(status_code=400, detail='Username must be between 3 and 20 characters')
    
    if check_if_username_exists(username):
        raise HTTPException(status_code=400, detail='Username already exists')

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

        print('SQL query')
        print(f'{hashed_password}: {len(hashed_password)}')
        print(f'{salt}: {len(salt)}')
        cursor.execute('INSERT INTO users(username, password_digest, password_salt, first_name, last_name) VALUES (%s, %s, %s, %s, %s);', (username, hashed_password, salt, first_name, last_name))

        conn.commit()

        cursor.close()
        conn.close()

    return {'username': username, 'first_name': first_name, 'last_name': last_name}

def login_user(username, password):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    result = cursor.fetchone()

    hashed_password = base64.b64decode(result[2])
    salt = base64.b64decode(result[3])

    print(hashed_password)
    print(salt)

    if pbkdf2_sha256.verify(str.join(str.strip(password), str.strip(salt)), hashed_password):
        return {'message': 'Login successful'}
    else:
        raise HTTPException(status_code=401, detail='Invalid login attempt')

    cursor.close()
    conn.close()

    print(result)

if __name__ == '__main__':
    if sys.argv[1] == 'register_user':
        register_user('test_user', 'P@ssword123', 'Test', 'User', test=True)
