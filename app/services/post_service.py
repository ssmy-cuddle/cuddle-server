from sqlalchemy.orm import Session
from models.posts import Posts
from models.postLikes import PostLike
from models.file import File
from schemas.post_schema import get_journey_response_items, get_journey_response, PostCreate, PostUpdate, PaginatedPostResponse, PostResponse, PaginatedPostResponseItems, PaginatedPostResponse2
from services.user_service import get_user_by_uid
from services.postComment_service import get_postComment_cnt
from services.postLike_service import get_like_reaction
from datetime import datetime
from pytz import timezone
from services.image_service import create_image, get_images
from schemas.image_schema import ImageCreate
from pydantic import parse_obj_as
from sqlalchemy import func, asc
from models.images import Images
import logging
from models.user import User
from models.file import File
from sqlalchemy import func, cast, Integer, Text


# 11.02 Paginator
from utils.paginator import Paginator  # Paginator 임포트
from sqlalchemy import or_, and_
from typing import List, Optional #11.02 Optional 추가

# 게시물 생성 함수
def create_post(db: Session, post: PostCreate):
    logging.info(f"Received request data: {post}")
    post_index = get_post_index(db)

    if post.images:
        for image in post.images:
            logging.info(f"Received request for images_id: {image}")
            # ImageItem을 ImageCreate로 변환

            image_create = ImageCreate(
                image_id=post_index,  # ImageItem의 id를 image_id로 사용
                file_id=str(image),   # file_id로 사용 (필요한 경우)
                file_url=None,      # url은 그대로 사용
                model='post'         # model에 image.name 사용
            )

            create_image(db, image_create)

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

    post_query = db.query(Posts).filter(Posts.post_id == post_id).first()  # 특정 post_id로 필터링

     # 이미지 정보 조회
    image_items = get_images(db, post_id)  # post_id에 해당하는 이미지들을 가져옴

    # 게시물 정보를 딕셔너리로 변환
    post_data = {
        "post_id": post_query.post_id,
        "uid": post_query.uid,
        "title": post_query.title,
        "content": post_query.content,
        "visibility": post_query.visibility,
        "created_at": post_query.created_at,
        "updated_at": post_query.updated_at,
        "is_deleted": 0,
        "post_likes": 0,
        "post_shares": 0
    }

    # 이미지 정보 추가
    post_data["images"] = image_items

    return post_data

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
        
        image_items = get_images(db, item.post_id)
        pydantic_item.images = image_items  # 하드코딩된 값 설정

        # 수동으로 각 필드 업데이트
        user_query = get_user_by_uid(db, item.uid)
        comment_cnt = get_postComment_cnt(db, item.post_id)
        reaction = get_like_reaction(db, item.post_id, item.uid)
        logging.info(f"Received request for viewer_id: {viewer_id}, item.uid :{item.uid}")
        
        pydantic_item.can_modify = "y" if (item.uid == viewer_id) else "n"
        pydantic_item.reactions = True if reaction else False # 게시글 좋아요 눌렀는지 여부
        pydantic_item.user_name = user_query.user_name  
        
        pydantic_item.comment_cnt = comment_cnt #댓글 수

        #프로필사진
        result = (
            db.query(User, File.file_name, File.file_url)
            .outerjoin(File, User.profile_image == File.file_id)
            .filter(User.uid == item.uid)
            .first()
        )

        if result:
            user, file_name, file_url = result

            pydantic_item.profile_image = file_url
            # pydantic_item.file_name = file_name
            # pydantic_item.file_url = file_url

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
    db: Session, 
    items: List[Posts]
):
    response_items = []
    
    for item in items:
        # from_orm을 이용하여 기본 모델 생성
        pydantic_item = get_journey_response_items.from_orm(item)
        
        # 수동으로 각 필드 업데이트
        image_items = get_images(db, item.post_id)
        pydantic_item.images = image_items  # 하드코딩된 값 설정
        
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


    response_items_pydantic = convert_get_journey_response_to_pydantic(db, response_items)

    return get_journey_response(
        items = response_items_pydantic
    )


def delete_post_by_id(db: Session, post: Posts):
    db.delete(post)
    db.commit()

def get_post_top(db: Session):
    subquery = (
        db.query(
            cast(Images.image_id, Text).label("image_id"),
            func.min(cast(Images.file_id, Text)).label("first_file_id")  # file_id를 Text로 캐스팅
        )
        .group_by(Images.image_id)
        .subquery()
    )

    # 조인 쿼리 작성 (select_from을 사용하여 명시적으로 조인 순서 지정)
    result = (
        db.query(Posts, File.file_name, File.file_url)
        .select_from(Posts)  # 조인을 시작할 기준 테이블을 명시적으로 설정
        .join(Images, cast(Images.image_id, Text) == cast(Posts.post_id, Text))  # Posts와 Images 조인
        .join(subquery, subquery.c.image_id == cast(Images.image_id, Text))  # 서브쿼리와 Images 조인 (타입 캐스팅)
        .join(File, subquery.c.first_file_id == cast(File.file_id, Text))  # 서브쿼리와 File 조인
        .limit(10)  # 상위 10개의 게시물만 가져오기
    ).all()
    
    if result:
        return result
    return None