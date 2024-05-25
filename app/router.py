from fastapi import APIRouter, Request, Cookie, Depends
from typing import Annotated, Union
from . import controller
from auth.auth_bearer import JWTBearer, JWTBearerAdmin

router = APIRouter()


@router.post('/user/create', dependencies=[Depends(JWTBearerAdmin())])
async def register_user(body: Request):
    payload = await body.json()
    if payload['is_admin']:
        return controller.register_user(payload['username'],
                                        payload['password'],
                                        payload['first_name'],
                                        payload['last_name'],
                                        payload['is_admin'])
    else:
        return controller.register_user(payload['username'],
                                        payload['password'],
                                        payload['first_name'],
                                        payload['last_name'])


@router.post('/user/login')
async def login_user(body: Request):
    payload = await body.json()

    return controller.login_user(payload['username'],
                                 payload['password'])


@router.get('/user/auth', dependencies=[Depends(JWTBearer())])
async def check_authentication_status():
    return {'message': 'Verified'}


@router.get('/admin/auth', dependencies=[Depends(JWTBearerAdmin())])
async def check_admin_authentication_status():
    return {'message': 'Verified'}


@router.get('/users/list', dependencies=[Depends(JWTBearerAdmin())])
async def list_users():
    pass


@router.get('/users/{user_id}', dependencies=[Depends(JWTBearerAdmin())])
async def get_user():
    pass


@router.put('/users/{user_id}', dependencies=[Depends(JWTBearerAdmin())])
async def update_user():
    pass


@router.delete('/users/{user_id"', dependencies=[Depends(JWTBearerAdmin())])
async def delete_user():
    pass


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

