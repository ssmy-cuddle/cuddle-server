from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.postLike_schema import PostLikeResponse, PostLikeCreate
from services.postLike_service import create_postLikes
from datetime import timedelta, datetime

router = APIRouter()

@router.post("/", response_model=PostLikeResponse)
def create_postLikes_endpoint(postLike: PostLikeCreate, db: Session = Depends(get_db)):
    return create_postLikes(db=db, postLike=postLike)
