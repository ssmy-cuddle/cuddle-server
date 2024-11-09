from sqlalchemy.orm import Session
from models.postComments import postComment
from schemas.postComment_schema import PostCommentCreate, PostCommentUpdate, PaginatedPostCommentResponseItems, PaginatedPostCommentResponse
from datetime import datetime
from pytz import timezone
from pydantic import parse_obj_as
from sqlalchemy import or_, and_
from typing import List, Optional 

# 댓글생성
def create_postComment(db: Session, postComment: PostCommentCreate):

    db_postComment = postComment(
        message=postComment.message,
        uid=postComment.uid,
        post_id=postComment.post_id,
        parent_id=postComment.parent_id
    )
    db.add(db_postComment)  # 게시물 추가 준비
    db.commit()  # 데이터베이스에 변경 사항 커밋
    db.refresh(db_postComment)  # 저장된 후 객체를 최신 상태로 갱신
    return db_postComment