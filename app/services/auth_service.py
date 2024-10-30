from sqlalchemy.orm import Session
from models.tokens import Token
from schemas.token_schema import TokenCreate, TokenUpdate
from datetime import datetime

def create_tokens(db: Session, token_data: TokenCreate) -> Token:

    print(token_data)

    new_token = Token(
        uid=token_data["uid"],
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        provider=token_data["provider"],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token

def get_tokens_by_user_id(db: Session, user_id: str) -> Token:
    return db.query(Token).filter(Token.user_id == user_id).first()

def update_tokens(db: Session, user_id: str, token_data: TokenUpdate) -> Token:
    token = db.query(Token).filter(Token.user_id == user_id).first()
    if token:
        token.access_token = token_data.access_token
        token.refresh_token = token_data.refresh_token
        token.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(token)
    return token

def delete_tokens_by_user_id(db: Session, user_id: str) -> None:
    token = db.query(Token).filter(Token.uid == user_id).first()
    if token:
        db.delete(token)
        db.commit()

def get_token_by_refresh_token(db: Session, refresh_token: str) -> Token:
    return db.query(Token).filter(Token.refresh_token == refresh_token).first()
