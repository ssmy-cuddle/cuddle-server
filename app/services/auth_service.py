from sqlalchemy.orm import Session
from models.user import User
from models.pets import Pet
from schemas.user_schema import UserCreate
from utils.hashing import Hash

def create_user(db: Session, user: UserCreate):
    hashed_password = Hash.get_password_hash(user.password)
    db_user = User(uid=user.uid, user_name=user.user_name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
