from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# User 테이블의 기본 스키마
class UserBase(BaseModel):
    username: str  # 사용자 이름
    email: EmailStr  # 이메일 주소
    bio: Optional[str] = None  # 프로필 설명
    phone_number: Optional[str] = None  # 전화번호

# User 생성 시 사용되는 스키마
class UserCreate(UserBase):
    password: str  # 비밀번호 (필수)
    provider: str  # 소셜 로그인 제공자 (카카오, 구글, 애플 중 하나)
    provider_id: str  # 소셜 제공자의 유니크한 ID

# User 업데이트 시 사용되는 스키마
class UserUpdate(UserBase):
    status: Optional[str] = None  # 사용자 상태 (활성, 비활성, 차단)
    last_login: Optional[datetime] = None  # 마지막 로그인 시간
    email_verified: Optional[bool] = None  # 이메일 인증 여부

# User 조회 시 반환되는 스키마
class UserOut(UserBase):
    user_id: int  # 사용자 ID
    created_at: datetime  # 생성 시간
    updated_at: datetime  # 수정 시간

    class Config:
        orm_mode = True  # ORM 객체를 Pydantic 모델로 변환 가능

# Post 테이블의 기본 스키마
class PostBase(BaseModel):
    title: Optional[str] = None  # 게시글 제목
    content: Optional[str] = None  # 게시글 내용
    visibility: Optional[str] = None  # 게시글 공개 범위

# Post 생성 시 사용되는 스키마
class PostCreate(PostBase):
    pass  # 별도 추가 필드는 없음

# Post 업데이트 시 사용되는 스키마
class PostUpdate(PostBase):
    is_deleted: Optional[bool] = None  # 삭제 여부

# Post 조회 시 반환되는 스키마
class PostOut(PostBase):
    post_id: int  # 게시글 ID
    user_id: int  # 작성자 ID
    created_at: datetime  # 생성 시간
    updated_at: datetime  # 수정 시간

    class Config:
        orm_mode = True  # ORM 객체를 Pydantic 모델로 변환 가능

# Comment 테이블의 기본 스키마
class CommentBase(BaseModel):
    content: str  # 댓글 내용

# Comment 생성 시 사용되는 스키마
class CommentCreate(CommentBase):
    parent_comment_id: Optional[int] = None  # 부모 댓글 ID (대댓글의 경우)

# Comment 업데이트 시 사용되는 스키마
class CommentUpdate(CommentBase):
    is_deleted: Optional[bool] = None  # 삭제 여부

# Comment 조회 시 반환되는 스키마
class CommentOut(CommentBase):
    comment_id: int  # 댓글 ID
    post_id: int  # 게시글 ID
    user_id: int  # 작성자 ID
    created_at: datetime  # 생성 시간
    updated_at: datetime  # 수정 시간

    class Config:
        orm_mode = True  # ORM 객체를 Pydantic 모델로 변환 가능

# PostImage 테이블의 기본 스키마
class PostImageBase(BaseModel):
    image_url: str  # 이미지 URL
    order: Optional[int] = None  # 이미지 순서
    alt_text: Optional[str] = None  # 대체 텍스트

# PostImage 생성 시 사용되는 스키마
class PostImageCreate(PostImageBase):
    post_id: int  # 게시글 ID (필수)

# PostImage 조회 시 반환되는 스키마
class PostImageOut(PostImageBase):
    image_id: int  # 이미지 ID
    created_at: datetime  # 생성 시간

    class Config:
        orm_mode = True  # ORM 객체를 Pydantic 모델로 변환 가능

# PostLike 테이블의 기본 스키마
class PostLikeBase(BaseModel):
    pass  # 특별히 추가할 필드 없음

# PostLike 생성 시 사용되는 스키마
class PostLikeCreate(PostLikeBase):
    post_id: int  # 게시글 ID (필수)
    user_id: int  # 사용자 ID (필수)

# PostLike 조회 시 반환되는 스키마
class PostLikeOut(PostLikeBase):
    like_id: int  # 좋아요 ID
    created_at: datetime  # 생성 시간

    class Config:
        orm_mode = True  # ORM 객체를 Pydantic 모델로 변환 가능

# CommentLike 테이블의 기본 스키마
class CommentLikeBase(BaseModel):
    pass  # 특별히 추가할 필드 없음

# CommentLike 생성 시 사용되는 스키마
class CommentLikeCreate(CommentLikeBase):
    comment_id: int  # 댓글 ID (필수)
    user_id: int  # 사용자 ID (필수)

# CommentLike 조회 시 반환되는 스키마
class CommentLikeOut(CommentLikeBase):
    like_id: int  # 좋아요 ID
    created_at: datetime  # 생성 시간

    class Config:
        orm_mode = True  # ORM 객체를 Pydantic 모델로 변환 가능

# Share 테이블의 기본 스키마
class ShareBase(BaseModel):
    shared_with: Optional[str] = None  # 공유된 대상
    platform: Optional[str] = None  # 공유된 플랫폼

# Share 생성 시 사용되는 스키마
class ShareCreate(ShareBase):
    post_id: int  # 게시글 ID (필수)
    user_id: int  # 사용자 ID (필수)

# Share 조회 시 반환되는 스키마
class ShareOut(ShareBase):
    share_id: int  # 공유 ID
    created_at: datetime  # 생성 시간

    class Config:
        orm_mode = True  # ORM 객체를 Pydantic 모델로 변환 가능
