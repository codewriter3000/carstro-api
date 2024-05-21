from .models import connect
from fastapi import HTTPException

import re


def register_user(username, password, first_name, last_name):
    if username is None or password is None or first_name is None or last_name is None:
        raise HTTPException(status_code=400, detail='Missing required field')

    if len(username) < 3 or len(username) > 20:
        raise HTTPException(status_code=400, detail='Username must be between 3 and 20 characters')

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

    
