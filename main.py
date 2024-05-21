from app.model import migrate
from fastapi import FastAPI

import sys

app = FastAPI()

app.include_router(app.router)

if __name__ == '__main__':
    if not sys.argv[1]:
        print('Incorrect usage of python main.py')

    if sys.argv[1] == 'migrate':
        print('Migration beginning')
        migrate()
