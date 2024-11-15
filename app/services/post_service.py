from sqlalchemy.orm import Session
import hashlib
import random
import string
from fastapi import APIRouter, UploadFile, File as FastAPIFile, HTTPException, Depends
from models.posts import Posts
from models.postLikes import PostLike
from schemas.post_schema import get_journey_response_items, get_journey_response, PostCreate, PostUpdate, PaginatedPostResponse, PostResponse, PaginatedPostResponseItems, PaginatedPostResponse2
from services.user_service import get_user_by_uid
from services.s3_service import upload_file_to_s3
from services.postComment_service import get_postComment_cnt
from services.postLike_service import get_like_reaction
from datetime import datetime
from pytz import timezone
from pydantic import parse_obj_as
from sqlalchemy import func, asc
import logging
from fastapi import BackgroundTasks

from models.file import File  # 올바른 File 모델 임포트
from schemas.file_schema import FileCreate
from schemas.image_schema import ImageCreate, ImageResponse

# 11.02 Paginator
from utils.paginator import Paginator  # Paginator 임포트
from sqlalchemy import or_, and_
from typing import List, Optional #11.02 Optional 추가

#11.15 파일업로드
def generate_hashed_filename(original_filename: str) -> str:
    if not isinstance(original_filename, str):
        raise ValueError("The original filename must be a string.")

    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    hash_object = hashlib.sha256(f"{original_filename}_{random_suffix}".encode())
    return hash_object.hexdigest()

async def upload_file(db: Session, uid: str, file: UploadFile = FastAPIFile(...) ):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="File must have a valid filename")

        # 파일 이름 해시화
        hashed_filename = generate_hashed_filename(file.filename)
        s3_filename = f"uploads/{hashed_filename}"

        # S3에 파일 업로드
        file_url = await upload_file_to_s3(file, s3_filename)

        # 데이터베이스에 파일 정보 저장
        file_record = FileCreate(
            file_name=hashed_filename,
            file_url=file_url,
            uid=uid
        )
        new_file = File(**file_record.dict())
        db.add(new_file)
        db.commit()
        db.refresh(new_file)

        return {"file_id": new_file.file_id, "file_url": file_url}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 게시물 생성 함수
async def create_post(db: Session, post: PostCreate):
    post_index = get_post_index(db)

    if post.images:
        for item in post.images:
            await upload_file(db, post.uid, item)
        

    db_post = Posts(
        post_id=post_index,
        uid=post.uid,
        title=post.title,
        content=post.content,
        visibility=post.visibility,
    )
    db.add(db_post)  # 게시물 추가 준비
    db.commit()  # 데이터베이스에 변경 사항 커밋
    db.refresh(db_post)  # 저장된 후 객체를 최신 상태로 갱신
    return db_post

def get_post_index(db: Session) -> str:
    str_date = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S') #이거바꾸니까 서버 죽음
    seq = 0

    while True:
        seq += 1
        str_seq = str(seq).zfill(4)
        str_index = str_date + str_seq

        exists = True if db.query(Posts).filter(Posts.post_id == str_index).one_or_none() else False

        if not exists:
            return str_index


# 특정 게시물 조회 함수
def get_post_by_id(db: Session, post_id: str):
    return db.query(Posts).filter(Posts.post_id == post_id).first()  # 특정 post_id로 필터링

# 특정 게시물 수정 함수
def update_post_by_id(db: Session, post: Posts, post_update: PostUpdate):
    if post_update.title is not None:
        post.title = post_update.title
    if post_update.content is not None:
        post.content = post_update.content
    if post_update.visibility is not None:
        post.visibility = post_update.visibility    

    db.commit()  # 수정된 내용을 데이터베이스에 반영
    db.refresh(post)  # 저장된 후 객체를 최신 상태로 갱신
    return post

# 특정 게시물 수정 함수
def update_post_like_cnt(db: Session, post: Posts, post_likes: Optional[str] = None):
    if post_likes is not None:
        post.post_likes = post_likes

    db.commit()  # 수정된 내용을 데이터베이스에 반영
    db.refresh(post)  # 저장된 후 객체를 최신 상태로 갱신
    return post

# 11.02 게시물 페이지네이션 조회 함수
def get_paginated_posts(
    db: Session, 
    uid: str, 
    viewer_id: str,
    cursor : Optional[str] = None,
    limit: int = 10, 
    is_friend: Optional[bool] = None
)-> PaginatedPostResponse:
    
    query = db.query(Posts)

    # 가시성 필터 설정
    if viewer_id:
        visibility_filter = or_(
            Posts.uid == viewer_id,  # 본인의 게시물은 모두 조회 가능 private 포함
            Posts.visibility == 'public',  # 공개 게시물은 모두 조회 가능
            (is_friend and Posts.visibility == 'friends')  # 친구일 경우 친구에게만 공개된 게시물도 조회 가능
        )
        query = query.filter(visibility_filter)
    else:
        query = query.filter(Posts.visibility == 'public')

    # Paginator 인스턴스 생성 및 페이지네이션 수행
    paginator = Paginator(Posts, query)
    paginated_result = paginator.get_paginated_result(
        cursor=cursor,
        direction = "desc",
        sorts=["-created_at"],  # 가장 최근에 작성된 게시물부터 조회
        limit=limit
    )
    print(paginated_result)
    # PostResponse로 변환
    response_items = [
        PaginatedPostResponseItems(
            post_id=item.post_id,
            uid=item.uid,
            title=item.title,
            content=item.content,
            # visibility=item.visibility,
            # postLike_cnt=item.is_deleted,
            # comment_cnt=item.post_likes,
        )
        for item in paginated_result.items
    ]


    return PaginatedPostResponse(
        items=response_items,  # 현재 페이지의 게시물 리스트
        has_more=paginated_result.has_more,  # Paginator에서 이미 계산된 has_more 사용
        next_cursor=paginated_result.next_cursor
        #is_follow = y
    )

def convert_posts_to_pydantic(db: Session, items: List[Posts], viewer_id: str) -> List[PaginatedPostResponseItems]:
    response_items = []
    
    for item in items:
        # from_orm을 이용하여 기본 모델 생성
        pydantic_item = PaginatedPostResponseItems.from_orm(item)
        
        # 수동으로 각 필드 업데이트
        user_query = get_user_by_uid(db, item.uid)
        comment_cnt = get_postComment_cnt(db, item.post_id)
        reaction = get_like_reaction(db, item.post_id, item.uid)
        logging.info(f"Received request for viewer_id: {viewer_id}, item.uid :{item.uid}")
        pydantic_item.can_modify = "y" if (item.uid == viewer_id) else "n"
        pydantic_item.reactions = True if reaction else False # 게시글 좋아요 눌렀는지 여부
        pydantic_item.user_name = user_query.user_name  
        pydantic_item.profile_image = user_query.profile_image 
        pydantic_item.images = [None] #게시글이미지
        pydantic_item.comment_cnt = comment_cnt #댓글 수
        
        response_items.append(pydantic_item)
        
    return response_items

# 11.06 게시물 페이지네이션 조회 함수
def get_paginated_posts2(
    db: Session, 
    viewer_id: str,
    cursor : Optional[str] = None,
    limit: int = 10, 
    direction: str = "after"
)-> PaginatedPostResponse2: 
    
    query = db.query(Posts)

    if cursor is not None:
        query = query.filter(Posts.post_id < cursor)

    query = query.order_by(Posts.post_id.desc())

    items = query.limit(limit + 1).all()
    has_more = len(items) > limit
    response_items = items[:limit]
    next_cursor = response_items[-1].post_id if has_more and response_items else None

    logging.info(f"Received request for viewer_id: {viewer_id}")

    response_items_pydantic = convert_posts_to_pydantic(db, response_items, viewer_id)

    return PaginatedPostResponse2(
        items=response_items_pydantic , 
        has_more=has_more,
        next_cursor=next_cursor
    )

def convert_get_journey_response_to_pydantic(
    items: List[Posts]
):
    response_items = []
    
    for item in items:
        # from_orm을 이용하여 기본 모델 생성
        pydantic_item = get_journey_response_items.from_orm(item)
        
        # 수동으로 각 필드 업데이트
        pydantic_item.images = [None]  # 하드코딩된 값 설정
        
        response_items.append(pydantic_item)
        
    return response_items

def get_journey(
    db: Session, 
    viewer_id: str,
    inqr_date: str
): 
    query = db.query(Posts)
    query = query.filter(Posts.uid == viewer_id)
    query = query.filter(func.to_char(Posts.created_at, 'YYYYMMDD') == inqr_date)
    response_items = query.order_by(asc(Posts.created_at))


    response_items_pydantic = convert_get_journey_response_to_pydantic(response_items)

    return get_journey_response(
        items = response_items_pydantic
    )


def delete_post_by_id(db: Session, post: Posts):
    db.delete(post)
    db.commit()