from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from typing import List 
from schemas.user_schema import UserCreate, UserResponse
from services.auth_service import create_user
from services.user_service import get_user_by_uid, get_user_by_email, get_user_exists_by_uid
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

@router.post("/check-id", response_model=None)
def check_id_exists(uid: str, db: Session = Depends(get_db)):
    user_exists = get_user_exists_by_uid(db, uid)

    if len(uid) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status_code": status.HTTP_400_BAD_REQUEST,
                "error_code": "INVALID_LENGTH",
                "msg": "ID의 길이가 50자를 초과했습니다."
            }
        )

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status_code": status.HTTP_409_CONFLICT,
                "error_code": "ALREADY_EXISTS",
                "msg": "존재하는 계정입니다."
            }
        )

    return {
        "uid": uid,
        "exists": False,
    }