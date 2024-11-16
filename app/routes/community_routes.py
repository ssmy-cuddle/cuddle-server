
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from typing import List
from services.post_service import get_post_top
from schemas.community_schema import CommunityResponse

router = APIRouter()

@router.get("/top-posts", response_model=List[CommunityResponse])
def read_top_posts(db: Session = Depends(get_db)):
    posts = get_post_top(db)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found"
        )

    # 결과 데이터 가공
    response = [
        CommunityResponse(
            post_id=post.post_id,
            uid=post.uid,
            title=post.title,
            content=post.content,
            file_name=file_name,
            file_url=file_url
        )
        for post, file_name, file_url in posts
    ]

    return response