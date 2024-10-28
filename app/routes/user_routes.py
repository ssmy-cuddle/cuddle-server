from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from typing import List 
from schemas.user_schema import UserCreate, UserResponse, UserProfileUpdate
from schemas.pet_schema import PetResponse
from services.user_service import create_user, get_user_by_uid, get_user_by_email, update_user_profile_by_uid, get_pets_by_user_id
from utils.hashing import Hash
from utils.jwt import create_access_token, create_refresh_token, verify_refresh_token
from core.config import settings
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user_uid = get_user_by_uid(db, user.uid)
    existing_user_email = get_user_by_email(db, user.email)
    if existing_user_uid or existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="존재하는 계정입니다."
        )
    return create_user(db=db, user=user)

@router.post("/login", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_uid(db, form_data.username)
    if not user or not Hash.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.uid}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=7)
    refresh_token = create_refresh_token(
        data={"sub": user.uid}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh-token", response_model=dict)
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        uid = verify_refresh_token(refresh_token)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_uid(db, uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.uid}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/{uid}", response_model=UserResponse)
def get_user_profile(uid: str, db: Session = Depends(get_db)):
    user = get_user_by_uid(db, uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/{uid}/pets", response_model=List[PetResponse])
def get_pets_by_user_id_endpoint(uid: str, db: Session = Depends(get_db)):
    pets = get_pets_by_user_id(db, uid)
    if not pets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pets found for this user"
        )
    return pets

@router.patch("/profile/{uid}", response_model=UserResponse)
def update_user_profile(uid: str, profile_update: UserProfileUpdate, db: Session = Depends(get_db)):
    user = get_user_by_uid(db, uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    updated_user = update_user_profile_by_uid(db, user, profile_update)
    return updated_user