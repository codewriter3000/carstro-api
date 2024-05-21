from fastapi import FastAPI

app = FastAPI()


@app.post('/user/create')
async def register_user():
    pass

@app.post('/user/login')
async def login_user():
    pass

@app.get('/users/list')
async def list_users():
    pass

@app.get('/users/{user_id}')
async def get_user():
    pass

@app.put('/users/{user_id}')
async def update_user():
    pass

@app.delete('/users/{user_id"')
async def delete_user():
    pass

@app.post('/role')
async def create_role():
    pass

@app.get('/roles')
async def list_roles():
    pass

@app.get('/roles/{role_id}')
async def get_role():
    pass

@app.put('/roles/{role_id}')
async def update_role():
    pass

@app.delete('/roles/{role_id}')
async def delete_role():
    pass

