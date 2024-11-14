from sqlalchemy.orm import Session
from models.postLikes import PostLike
from schemas.postLike_schema import PostLikeResponse, PostLikeCreate
from datetime import datetime
from pytz import timezone
from pydantic import parse_obj_as
from sqlalchemy import or_, and_
from typing import List, Optional 

# 댓글생성
def create_postLikes( 
    postLike : PostLikeCreate,
    db: Session
):

    db_postLike = PostLike(
        post_id=postLike.post_id,
        uid=postLike.uid,
    )

    db.add(db_postLike)  # 게시물 추가 준
    db.commit()  # 데이터베이스에 변경 사항 커밋
    db.refresh(db_postLike)  # 저장된 후 객체를 최신 상태로 갱신
    return db_postLike

def get_like_reaction(db: Session, post_id: str, viewer_id: str):
    query = db.query(PostLike).filter(PostLike.post_id == post_id)
    return query.filter(PostLike.uid == viewer_id).first()

def delete_postlikes_by_id(db: Session, postlike: PostLike):
    db.delete(postlike)
    db.commit()