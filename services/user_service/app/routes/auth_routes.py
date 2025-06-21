from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
import base64
import requests
from urllib.parse import urlencode

from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.user import User

router = APIRouter()

# Environment variables
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPES = "user-read-private user-read-email"

# /auth/login: Generate Spotify login URL
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

# /auth/callback: Handle Spotify redirect and save user
from fastapi.responses import RedirectResponse

@router.get("/auth/callback")
def auth_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    # Step 1: Exchange code for token
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    token_response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {b64_auth_str}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        }
    )

    if token_response.status_code != 200:
        print("Token exchange failed:", token_response.text)
        raise HTTPException(status_code=token_response.status_code, detail="Token exchange failed")

    token_data = token_response.json()
    access_token = token_data["access_token"]
    refresh_token = token_data.get("refresh_token")

    # Step 2: Get Spotify user profile
    user_response = requests.get(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if user_response.status_code != 200:
        raise HTTPException(status_code=user_response.status_code, detail="Failed to fetch user profile")

    profile = user_response.json()

    # Step 3: Save or update user in DB
    db_user = db.query(User).filter(User.id == profile["id"]).first()

    if db_user:
        db_user.display_name = profile.get("display_name")
        db_user.email = profile.get("email")
        db_user.country = profile.get("country")
        db_user.access_token = access_token
        db_user.refresh_token = refresh_token
    else:
        db_user = User(
            id=profile["id"],
            display_name=profile.get("display_name"),
            email=profile.get("email"),
            country=profile.get("country"),
            access_token=access_token,
            refresh_token=refresh_token
        )
        db.add(db_user)

    db.commit()

    # Step 4: Redirect to frontend dashboard with user_id
    dashboard_url = f"http://localhost:3000/dashboard?user_id={db_user.id}"
    return RedirectResponse(url=dashboard_url, status_code=302)


@router.get("/me/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "display_name": user.display_name,
        "email": user.email,
        "country": user.country
    }
