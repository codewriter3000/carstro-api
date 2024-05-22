from fastapi import APIRouter, Request
from . import controller

router = APIRouter()


@router.post('/user/create')
async def register_user(body: Request):
    payload = await body.json()

    print(payload)
    return controller.register_user(payload['username'], 
                                    payload['password'], 
                                    payload['first_name'], 
                                    payload['last_name'])

@router.post('/user/login')
async def login_user(body: Request):
    payload = await body.json()

    return controller.login_user(payload['username'],
                                 payload['password'])

@router.get('/users/list')
async def list_users():
    pass

@router.get('/users/{user_id}')
async def get_user():
    pass

@router.put('/users/{user_id}')
async def update_user():
    pass

@router.delete('/users/{user_id"')
async def delete_user():
    pass

@router.post('/role')
async def create_role():
    pass

@router.get('/roles')
async def list_roles():
    pass

@router.get('/roles/{role_id}')
async def get_role():
    pass

@router.put('/roles/{role_id}')
async def update_role():
    pass

@router.delete('/roles/{role_id}')
async def delete_role():
    pass

