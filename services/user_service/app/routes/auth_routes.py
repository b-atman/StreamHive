# services/user_service/app/routes/auth_routes.py

from fastapi import APIRouter
import os
from urllib.parse import urlencode

router = APIRouter()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPES = "user-read-private user-read-email"

@router.get("/auth/login")
def login():
    query_params = urlencode({
        "response_type": "code",
        "client_id": SPOTIFY_CLIENT_ID,
        "scope": SCOPES,
        "redirect_uri": REDIRECT_URI
    })
    spotify_auth_url = f"https://accounts.spotify.com/authorize?{query_params}"
    return {"auth_url": spotify_auth_url}
