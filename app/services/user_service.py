from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate
from utils.hashing import Hash

def create_user(db: Session, user: UserCreate):
    hashed_password = Hash.get_password_hash(user.password)
    db_user = User(uid=user.uid, user_name=user.user_name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_uid(db: Session, uid: str):
    return db.query(User).filter(User.uid == uid).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not Hash.verify_password(password, user.password):
        return None
    return user
