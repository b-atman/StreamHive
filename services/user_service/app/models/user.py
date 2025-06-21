# services/user_service/app/models/user.py

from sqlalchemy import Column, String
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # Spotify user ID
    display_name = Column(String)
    email = Column(String, unique=True, index=True)
    country = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
