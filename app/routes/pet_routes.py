from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.pet_schema import PetCreate, PetResponse, PetUpdate, PetResponseWithFile
from services.pet_service import create_pet, get_pet_by_id, update_pet_by_id, delete_pet_by_id, get_pet_by_id_with_file
from typing import List

router = APIRouter()

@router.post("/", response_model=PetResponse)
def create_pet_endpoint(pet: PetCreate, db: Session = Depends(get_db)):
    return create_pet(db=db, pet=pet)

@router.get("/{pet_id}", response_model=PetResponseWithFile)
def get_pet_endpoint(pet_id: int, db: Session = Depends(get_db)):
    pet = get_pet_by_id_with_file(db, pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    return pet 

@router.patch("/{pet_id}", response_model=PetResponse)
def update_pet_endpoint(pet_id: int, pet_update: PetUpdate, db: Session = Depends(get_db)):
    pet = get_pet_by_id(db, pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    updated_pet = update_pet_by_id(db, pet, pet_update, pet_id)

    print(updated_pet)

    return updated_pet

@router.delete("/{pet_id}", response_model=dict)
def delete_pet_endpoint(pet_id: int, db: Session = Depends(get_db)):
    pet = get_pet_by_id(db, pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    delete_pet_by_id(db, pet)
    return {"detail": "Pet deleted successfully"}
