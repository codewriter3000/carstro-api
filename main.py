from app.model import migrate
from fastapi import FastAPI

app = FastAPI()

app.include_router(app.router)
