from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from schemas.user_schema import UserCreate, UserResponse, OAuthUser
from services.user_service import create_user, get_user_by_email, authenticate_oauth_user

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, email=user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )
    user = create_user(db, user_create)
    return user

@router.post("/oauth/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def oauth_signup(oauth_user: OAuthUser, db: Session = Depends(get_db)):
    # Authenticate the user using the provided OAuth token
    user_data = authenticate_oauth_user(oauth_user)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OAuth credentials."
        )
    # Check if the user is already registered
    existing_user = get_user_by_email(db, email=user_data.email)
    if existing_user:
        return existing_user
    # Create a new user based on OAuth data
    user = create_user(db, UserCreate(username=user_data.username, email=user_data.email, password="oauth_placeholder"))
    return user

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user