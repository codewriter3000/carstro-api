from fastapi import APIRouter, Request, Cookie, Depends
from typing import Annotated, Union
from . import controller
from auth.auth_bearer import JWTBearer, JWTBearerAdmin
from .controller import list_all_users, get_user_by_user_id, update_user_by_id, delete_user_by_id

router = APIRouter()


@router.post('/user/create') #, dependencies=[Depends(JWTBearerAdmin())])
async def register_user(body: Request):
    payload = await body.json()

    return controller.register_user(payload['username'],
                                    payload['password'],
                                    payload['first_name'],
                                    payload['last_name'],
                                    payload['is_admin'],
                                    payload['is_enabled'])


@router.post('/user/login')
async def login_user(body: Request):
    payload = await body.json()

    return controller.login_user(payload['username'],
                                 payload['password'])


@router.post('/user/logout')
async def logout_user():
    return controller.logout_user()


@router.get('/user/auth', dependencies=[Depends(JWTBearer())])
async def check_authentication_status():
    return {'is_admin': True, 'message': 'Verified'}


@router.get('/admin/auth', dependencies=[Depends(JWTBearerAdmin())])
async def check_admin_authentication_status():
    return {'is_admin': True, 'message': 'Verified'}


@router.get('/users/list')#, dependencies=[Depends(JWTBearerAdmin())])
async def list_users():
    return list_all_users()


@router.get('/users/{user_id}', dependencies=[Depends(JWTBearerAdmin())])
async def get_user(user_id: int):
    return get_user_by_user_id(user_id)


@router.put('/users/{user_id}')#, dependencies=[Depends(JWTBearerAdmin())])
async def update_user(user_id: int, body: Request):
    payload = await body.json()

    print(payload)

    return update_user_by_id(user_id, payload['username'],
                             payload['first_name'],
                             payload['last_name'],
                             payload['is_admin'],
                             payload['is_enabled'])


@router.delete('/users/{user_id}')#, dependencies=[Depends(JWTBearerAdmin())])
async def delete_user(user_id: int):
    return delete_user_by_id(user_id)


@router.post('/role', dependencies=[Depends(JWTBearerAdmin())])
async def create_role():
    pass


@router.get('/roles', dependencies=[Depends(JWTBearerAdmin())])
async def list_roles():
    pass


@router.get('/roles/{role_id}', dependencies=[Depends(JWTBearerAdmin())])
async def get_role():
    pass


@router.put('/roles/{role_id}', dependencies=[Depends(JWTBearerAdmin())])
async def update_role():
    pass


@router.delete('/roles/{role_id}', dependencies=[Depends(JWTBearerAdmin())])
async def delete_role():
    pass

