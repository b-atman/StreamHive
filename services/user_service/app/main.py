# services/user_service/app/main.py

from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

# ✅ DEBUG: Confirm .env is loading
print("REDIRECT_URI from .env:", os.getenv("REDIRECT_URI"))
print("SPOTIFY_CLIENT_ID from .env:", os.getenv("SPOTIFY_CLIENT_ID"))

from app.routes import auth_routes

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include auth routes
app.include_router(auth_routes.router)

@app.get("/")
def read_root():
    return {"message": "User Service is running"}


# services/user_service/app/main.py

from app.db.database import Base, engine
from app.models.user import User  # Ensure the model is imported

# Create tables
Base.metadata.create_all(bind=engine)
