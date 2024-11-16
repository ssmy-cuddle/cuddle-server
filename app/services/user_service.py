from sqlalchemy.orm import Session
from models.user import User
from models.pets import Pet
from models.file import File
from schemas.user_schema import UserCreate, UserProfileUpdate, UserResponse, UserResponseWithFile
from utils.hashing import Hash
from utils.nickname import getNickname

async def create_user(db: Session, user: UserCreate):
    hashed_password = Hash.get_password_hash(user.password)
    nickname = await getNickname()
    
    db_user = User(uid=user.uid, user_name=nickname, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_uid(db: Session, uid: str):
    return db.query(User).filter(User.uid == uid).first()

def get_user_and_file_info(db: Session, uid: str):
    result = (
        db.query(User, File.file_name, File.file_url)
        .outerjoin(File, User.profile_image == File.file_id)
        .filter(User.uid == uid)
        .first()
    )

    print(result)

    if result:
        user, file_name, file_url = result
        # User와 File 정보를 통합한 딕셔너리 생성
        user_dict = {
            "uid": user.uid,
            "email": user.email,
            "user_name": user.user_name,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "status": user.status,
            "profile_intro": user.profile_intro,
            "profile_image": user.profile_image,
            "file_name": file_name,
            "file_url": file_url
        }
        # UserResponse 모델로 반환
        return UserResponseWithFile(**user_dict)
    
    return None

def get_user_exists_by_uid(db: Session, uid: str):
    return True if db.query(User).filter(User.uid == uid).one_or_none() else False

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not Hash.verify_password(password, user.password):
        return None
    return user

def update_user_profile_by_uid(db: Session, user: User, profile_update: UserProfileUpdate):
    if profile_update.profile_intro is not None:
        user.profile_intro = profile_update.profile_intro
    if profile_update.profile_image is not None:
        user.profile_image = profile_update.profile_image
    if profile_update.user_name is not None:
        user.user_name = profile_update.user_name
    
    db.commit()
    db.refresh(user)
    return user

def get_pets_by_user_id(db: Session, uid: str):
    return db.query(Pet).filter(Pet.uid == uid).all()