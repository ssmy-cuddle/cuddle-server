from pydantic import BaseModel
from typing import Optional
from datetime import date

class PetBase(BaseModel):
    uid: str
    name: str
    birthday: Optional[date] = None
    breed: Optional[str] = None
    adoption_date: Optional[date] = None
    separation_date: Optional[date] = None
    gender: Optional[str] = None
    neutered: Optional[bool] = None
    weight: Optional[float] = None
    description: Optional[str] = None

class PetCreate(PetBase):
    pass

class PetUpdate(BaseModel):
    name: Optional[str] = None
    birthday: Optional[date] = None
    breed: Optional[str] = None
    adoption_date: Optional[date] = None
    separation_date: Optional[date] = None
    gender: Optional[str] = None
    neutered: Optional[bool] = None
    weight: Optional[float] = None
    description: Optional[str] = None

class PetResponse(PetBase):
    pet_id: int

    class Config:
        from_attributes = True