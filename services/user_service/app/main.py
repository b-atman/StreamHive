# services/user_service/app/main.py

from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.routes import auth_routes

load_dotenv()

app = FastAPI()

# Include the auth routes
app.include_router(auth_routes.router)

@app.get("/")
def read_root():
    return {"message": "User Service is running"}
