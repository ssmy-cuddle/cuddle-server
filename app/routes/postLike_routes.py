from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.postLike_schema import PostLikeResponse, PostLikeCreate
from services.postLike_service import create_postLikes, delete_postlikes_by_id, get_like_reaction
from datetime import timedelta, datetime

router = APIRouter()

@router.post("/", response_model=PostLikeResponse)
def create_postLikes_endpoint(postLike: PostLikeCreate, db: Session = Depends(get_db)):
    return create_postLikes(db=db, postLike=postLike)

@router.delete("/{post_id}/{uid}", response_model=dict)
def delete_postLikes_endpoint(post_id: str, uid:str, db: Session = Depends(get_db)):
    reaction = get_like_reaction(db, post_id, uid )
    if not reaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Postlikes not found"
        )
    delete_postlikes_by_id(db, reaction)
    return {"detail": "likes deleted successfully"}
