from app.model import migrate
from fastapi import FastAPI
from app import router

app = FastAPI(debug=True)

app.include_router(router.router)
