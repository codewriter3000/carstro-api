from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import router
from dotenv import dotenv_values
config = dotenv_values('.env')

SECRET_KEY = config['SECRET_KEY']

app = FastAPI(debug=True)

origins = {
    'http://localhost:4321',
    '*'
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(router.router)
