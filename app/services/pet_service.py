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
        db.query(Pet)
        .filter(Pet.pet_id == pet_id)
        .first()
    )

    if result:
        return result
    return None

def get_pet_by_id_with_file(db: Session, pet_id: int):
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

def update_pet_by_id(db: Session, pet: Pet, pet_update: PetUpdate, pet_id: str):
    for key, value in pet_update.dict(exclude_unset=True).items():
        setattr(pet, key, value)
    
    print(pet)

    db.commit()
    db.refresh(pet)

    return pet

def delete_pet_by_id(db: Session, pet: Pet):
    db.delete(pet)
    db.commit()