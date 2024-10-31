from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.user_schema import UserCreate, UserResponse, UserIdExistsResponse, CheckUserId
from schemas.token_schema import TokenResponse, RefreshTokenResponse
from services.user_service import create_user, get_user_by_uid, get_user_by_email, get_user_exists_by_uid
from services.auth_service import create_tokens, get_token_by_refresh_token, delete_tokens_by_user_id
from utils.hashing import Hash
from utils.jwt import create_access_token, create_refresh_token
from core.config import settings
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from utils.error_code import ErrorCode, raise_error

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user_uid = get_user_by_uid(db, user.uid)
    existing_user_email = get_user_by_email(db, user.email)

    if existing_user_uid or existing_user_email:
        raise_error(ErrorCode.ALREADY_EXISTS)
    
    return create_user(db=db, user=user)

@router.post("/login", response_model=TokenResponse)
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

    create_tokens(db, token_data={
        "uid": user.uid,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "provider": "local"
    })

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh-token", response_model=RefreshTokenResponse)
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    # 리프레시 토큰을 데이터베이스에서 확인
    token_entry = get_token_by_refresh_token(db, refresh_token)
    if not token_entry:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    uid = token_entry.uid
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": uid}, expires_delta=access_token_expires
    )

    # 기존 토큰 정보를 업데이트
    token_entry.access_token = access_token
    token_entry.updated_at = datetime.utcnow()
    db.commit()

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/check-id", response_model=UserIdExistsResponse)
def check_id_exists(UserId: CheckUserId, db: Session = Depends(get_db)):
    user_exists = get_user_exists_by_uid(db, UserId.uid)

    if len(UserId.uid) > 50:
        raise_error(ErrorCode.INVALID_LENGTH)

    if user_exists:
        return {
            "uid": UserId.uid,
            "exists": True,
        }

    return {
        "uid": UserId.uid,
        "exists": False,
    }
