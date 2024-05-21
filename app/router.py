from fastapi import APIRouter
from . import controller

router = APIRouter()


@router.post('/user/create')
async def register_user(params):
    return controller.register_user(params.username, 
                                    params.password, 
                                    params.first_name, 
                                    params.last_name)

@router.post('/user/login')
async def login_user():
    pass

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

