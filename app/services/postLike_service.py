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
    post_id : str,  
    uid : str,
    db: Session
):

    db_postLike = PostLike(
        post_id=post_id,
        uid=uid,
    )

    db.add(db_postLike)  # 게시물 추가 준
    db.commit()  # 데이터베이스에 변경 사항 커밋
    db.refresh(db_postLike)  # 저장된 후 객체를 최신 상태로 갱신
    return db_postLike