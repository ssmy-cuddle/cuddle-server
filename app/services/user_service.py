from sqlalchemy.orm import Session
from typing import Optional

from schemas.user_schema import UserCreate, OAuthUser
from models import User
from db.session import get_db
from utils.hashing import Hasher
from utils.jwt import decode_token

# Create a new user
def create_user(db: Session, user_create: UserCreate) -> User:
    hashed_password = Hasher.get_password_hash(user_create.password)
    db_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
        full_name=user_create.full_name,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by email
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

# Authenticate OAuth user
def authenticate_oauth_user(oauth_user: OAuthUser) -> Optional[UserCreate]:
    user_data = decode_token(oauth_user.provider.access_token)
    if not user_data:
        return None
    return UserCreate(
        username=user_data.get("username"),
        email=user_data.get("email"),
        password="oauth_placeholder"  # OAuth users won't have a regular password
    )

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return Hasher.verify_password(plain_password, hashed_password)