from fastapi import FastAPI
from app.api import sample_routes

app = FastAPI()

app.include_router(sample_routes.router)