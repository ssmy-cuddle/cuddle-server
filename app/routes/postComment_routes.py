from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.postComment_schema import PostCommentCreate, PostCommentUpdate, PaginatedPostCommentResponse, PostCommentResponse
from services.postComment_service import create_postComment
from typing import List

router = APIRouter()

@router.post("/{post_id}", response_model=PostCommentResponse)
def create_postComment_endpoint(post_id: str, postComment: PostCommentCreate, db: Session = Depends(get_db)):
 
    return create_postComment(post_id=post_id, db=db, postComment=postComment)
