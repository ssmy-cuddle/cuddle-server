from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from typing import List 
from schemas.user_schema import UserResponse, UserProfileUpdate, UserResponseWithFile
from schemas.pet_schema import PetResponse
from services.user_service import get_user_by_uid, update_user_profile_by_uid, get_pets_by_user_id, get_user_and_file_info
router = APIRouter()

@router.get("/{uid}", response_model=UserResponseWithFile)
def get_user_profile(uid: str, db: Session = Depends(get_db)):
    user = get_user_and_file_info(db, uid)
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