from sqlalchemy.orm import Session
from models.pets import Pet
from models.file import File
from schemas.pet_schema import PetCreate, PetUpdate, PetResponse

def create_pet(db: Session, pet: PetCreate):
    db_pet = Pet(
        uid=pet.uid,
        name=pet.name,
        birthday=pet.birthday,
        breed=pet.breed,
        adoption_date=pet.adoption_date,
        separation_date=pet.separation_date,
        gender=pet.gender,
        neutered=pet.neutered,
        weight=pet.weight,
        description=pet.description
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

def get_pet_by_id(db: Session, pet_id: int):
    result = (
        db.query(Pet, File.file_name, File.file_url)
        .outerjoin(File, Pet.pet_img_id == File.file_id)
        .filter(Pet.pet_id == pet_id)
        .first()
    )

    if result:
        pet, file_name, file_url = result
        # User와 File 정보를 통합한 딕셔너리 생성
        pet_dict = {
            "pet_id": pet.pet_id,
            "uid": pet.uid,
            "name": pet.name,
            "birthday": pet.birthday,
            "breed": pet.breed,
            "adoption_date": pet.adoption_date,
            "separation_date": pet.separation_date,
            "gender": pet.gender,
            "neutered": pet.neutered,
            "weight": pet.weight,
            "description": pet.description,
            "pet_img_id": pet.pet_img_id,
            "file_name": file_name,
            "file_url": file_url
        }
        # UserResponse 모델로 반환
        return PetResponse(**pet_dict)
    
    return None

def update_pet_by_id(db: Session, pet: Pet, pet_update: PetUpdate):
    if pet_update.name is not None:
        pet.name = pet_update.name
    if pet_update.birthday is not None:
        pet.birthday = pet_update.birthday
    if pet_update.breed is not None:
        pet.breed = pet_update.breed
    if pet_update.adoption_date is not None:
        pet.adoption_date = pet_update.adoption_date
    if pet_update.separation_date is not None:
        pet.separation_date = pet_update.separation_date
    if pet_update.gender is not None:
        pet.gender = pet_update.gender
    if pet_update.neutered is not None:
        pet.neutered = pet_update.neutered
    if pet_update.weight is not None:
        pet.weight = pet_update.weight
    if pet_update.description is not None:
        pet.description = pet_update.description
    
    db.commit()
    db.refresh(pet)
    return pet

def delete_pet_by_id(db: Session, pet: Pet):
    db.delete(pet)
    db.commit()