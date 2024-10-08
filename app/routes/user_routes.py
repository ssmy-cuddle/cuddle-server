from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.user_schema import UserResponse, UserPatch
from services.user_service import UserService
from utils.jwt import verify_token

@router.get("/", response_model=List[UserResponse])
async def get_users(skip: int = None, limit: int = None, db: Session = Depends(get_db)):
    return await UserService(db).get_users(skip=skip, limit=limit)