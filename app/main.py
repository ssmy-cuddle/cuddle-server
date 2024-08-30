from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
import requests
from jose import JWTError, jwt


# FastAPI 인스턴스를 생성
app = FastAPI()

# 데이터베이스 세션을 얻기 위한 의존성 주입 함수
# 모든 요청마다 새로운 세션을 열고, 요청이 끝나면 세션을 닫음
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User 생성 엔드포인트
# 클라이언트로부터 UserCreate 스키마의 데이터를 받아 새로운 유저를 생성
# @app.post("/users/", response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # return crud.create_user(db=db, user=user)

# OAuth 2.0으로 로그인 및 회원 가입 처리
@app.post("/auth/oauth2login/")
def oauth2_login(provider: str, code: str, db: Session = Depends(get_db)):
    user_info = None

    if provider == "google":
        # Google의 Authorization Code를 통해 Access Token 요청
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": "GOOGLE_CLIENT_ID",  # Google API Console에서 발급받은 클라이언트 ID
            "client_secret": "GOOGLE_CLIENT_SECRET",  # 클라이언트 시크릿
            "redirect_uri": "YOUR_REDIRECT_URI",  # 리다이렉트 URI
            "grant_type": "authorization_code"
        }

        # Access Token 요청
        token_response = requests.post(token_url, data=token_data)
        if token_response.status_code == 200:
            access_token = token_response.json().get("access_token")

            # Access Token을 사용해 사용자 정보 요청
            user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
            user_info_response = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"})
            if user_info_response.status_code == 200:
                user_info = user_info_response.json()
        else:
            raise HTTPException(status_code=400, detail="Failed to fetch Google access token")

    elif provider == "kakao":
        # Kakao의 Authorization Code를 통해 Access Token 요청
        token_url = "https://kauth.kakao.com/oauth/token"
        token_data = {
            "code": code,
            "client_id": "KAKAO_CLIENT_ID",  # Kakao Developers에서 발급받은 클라이언트 ID
            "client_secret": "KAKAO_CLIENT_SECRET",  # 클라이언트 시크릿
            "redirect_uri": "YOUR_REDIRECT_URI",  # 리다이렉트 URI
            "grant_type": "authorization_code"
        }

        # Access Token 요청
        token_response = requests.post(token_url, data=token_data)
        if token_response.status_code == 200:
            access_token = token_response.json().get("access_token")

            # Access Token을 사용해 사용자 정보 요청
            user_info_url = "https://kapi.kakao.com/v2/user/me"
            user_info_response = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"})
            if user_info_response.status_code == 200:
                user_info = user_info_response.json()
        else:
            raise HTTPException(status_code=400, detail="Failed to fetch Kakao access token")

    # 사용자 정보로 회원 가입 또는 로그인 처리
    if user_info:
        provider_id = user_info.get("id")
        user = crud.get_user_by_provider_id(db=db, provider_id=provider_id)

        if not user:
            # 새로운 사용자라면 회원 가입 처리
            user_data = schemas.UserCreate(
                username=user_info.get("nickname", "Unknown"),
                email=user_info.get("email"),
                provider=provider,
                provider_id=provider_id
            )
            user = crud.create_user(db=db, user=user_data)

        # 로그인 처리 (필요한 경우 JWT 발급 등 추가 작업 가능)
        return {"message": "Login successful", "user": user}

    raise HTTPException(status_code=400, detail="Unable to fetch user information")

# 특정 유저 조회 엔드포인트
# 주어진 user_id에 해당하는 유저 정보를 반환
@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 유저 목록 조회 엔드포인트
# 다수의 유저 정보를 페이징하여 반환
@app.get("/users/", response_model=List[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# 유저 정보 업데이트 엔드포인트
# 주어진 user_id에 해당하는 유저의 정보를 업데이트
@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, user_update=user)

# 유저 삭제 엔드포인트
# 주어진 user_id에 해당하는 유저를 삭제
@app.delete("/users/{user_id}", response_model=schemas.UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Post 생성 엔드포인트
# 클라이언트로부터 PostCreate 스키마의 데이터를 받아 새로운 게시글을 생성
@app.post("/posts/", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post, user_id=user_id)

# 특정 게시글 조회 엔드포인트
# 주어진 post_id에 해당하는 게시글 정보를 반환
@app.get("/posts/{post_id}", response_model=schemas.PostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

# 게시글 목록 조회 엔드포인트
# 다수의 게시글 정보를 페이징하여 반환
@app.get("/posts/", response_model=List[schemas.PostOut])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

# 게시글 업데이트 엔드포인트
# 주어진 post_id에 해당하는 게시글의 정보를 업데이트
@app.put("/posts/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    return crud.update_post(db=db, post_id=post_id, post_update=post)

# 게시글 삭제 엔드포인트
# 주어진 post_id에 해당하는 게시글을 삭제
@app.delete("/posts/{post_id}", response_model=schemas.PostOut)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.delete_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

# Comment 생성 엔드포인트
# 클라이언트로부터 CommentCreate 스키마의 데이터를 받아 새로운 댓글을 생성
@app.post("/comments/", response_model=schemas.CommentOut)
def create_comment(comment: schemas.CommentCreate, user_id: int, post_id: int, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment, user_id=user_id, post_id=post_id)

# 특정 댓글 조회 엔드포인트
# 주어진 comment_id에 해당하는 댓글 정보를 반환
@app.get("/comments/{comment_id}", response_model=schemas.CommentOut)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

# 댓글 목록 조회 엔드포인트
# 특정 게시글에 대한 댓글 정보를 페이징하여 반환
@app.get("/comments/", response_model=List[schemas.CommentOut])
def read_comments(post_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    comments = crud.get_comments(db, post_id=post_id, skip=skip, limit=limit)
    return comments

# 댓글 업데이트 엔드포인트
# 주어진 comment_id에 해당하는 댓글의 정보를 업데이트
@app.put("/comments/{comment_id}", response_model=schemas.CommentOut)
def update_comment(comment_id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db)):
    return crud.update_comment(db=db, comment_id=comment_id, comment_update=comment)

# 댓글 삭제 엔드포인트
# 주어진 comment_id에 해당하는 댓글을 삭제
@app.delete("/comments/{comment_id}", response_model=schemas.CommentOut)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.delete_comment(db=db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


# PostImage 생성 엔드포인트
# 클라이언트로부터 PostImageCreate 스키마의 데이터를 받아 새로운 이미지 정보를 생성
@app.post("/post_images/", response_model=schemas.PostImageOut)
def create_post_image(post_image: schemas.PostImageCreate, db: Session = Depends(get_db)):
    return crud.create_post_image(db=db, post_image=post_image)

# 특정 이미지 조회 엔드포인트
# 주어진 image_id에 해당하는 이미지 정보를 반환
@app.get("/post_images/{image_id}", response_model=schemas.PostImageOut)
def read_post_image(image_id: int, db: Session = Depends(get_db)):
    db_post_image = crud.get_post_image(db, image_id=image_id)
    if db_post_image is None:
        raise HTTPException(status_code=404, detail="Post Image not found")
    return db_post_image

# 이미지 삭제 엔드포인트
# 주어진 image_id에 해당하는 이미지를 삭제
@app.delete("/post_images/{image_id}", response_model=schemas.PostImageOut)
def delete_post_image(image_id: int, db: Session = Depends(get_db)):
    db_post_image = crud.delete_post_image(db=db, image_id=image_id)
    if db_post_image is None:
        raise HTTPException(status_code=404, detail="Post Image not found")
    return db_post_image

# PostLike 생성 엔드포인트
# 클라이언트로부터 PostLikeCreate 스키마의 데이터를 받아 새로운 좋아요 정보를 생성
@app.post("/post_likes/", response_model=schemas.PostLikeOut)
def create_post_like(post_like: schemas.PostLikeCreate, db: Session = Depends(get_db)):
    return crud.create_post_like(db=db, post_like=post_like)

# 게시글 좋아요 삭제 엔드포인트
# 주어진 post_id와 user_id에 해당하는 좋아요 정보를 삭제
@app.delete("/post_likes/", response_model=schemas.PostLikeOut)
def delete_post_like(post_id: int, user_id: int, db: Session = Depends(get_db)):
    db_post_like = crud.delete_post_like(db=db, post_id=post_id, user_id=user_id)
    if db_post_like is None:
        raise HTTPException(status_code=404, detail="Post Like not found")
    return db_post_like

# CommentLike 생성 엔드포인트
# 클라이언트로부터 CommentLikeCreate 스키마의 데이터를 받아 새로운 댓글 좋아요 정보를 생성
@app.post("/comment_likes/", response_model=schemas.CommentLikeOut)
def create_comment_like(comment_like: schemas.CommentLikeCreate, db: Session = Depends(get_db)):
    return crud.create_comment_like(db=db, comment_like=comment_like)

# 댓글 좋아요 삭제 엔드포인트
# 주어진 comment_id와 user_id에 해당하는 좋아요 정보를 삭제
@app.delete("/comment_likes/", response_model=schemas.CommentLikeOut)
def delete_comment_like(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    db_comment_like = crud.delete_comment_like(db=db, comment_id=comment_id, user_id=user_id)
    if db_comment_like is None:
        raise HTTPException(status_code=404, detail="Comment Like not found")
    return db_comment_like

# Share 생성 엔드포인트
# 클라이언트로부터 ShareCreate 스키마의 데이터를 받아 새로운 공유 정보를 생성
@app.post("/shares/", response_model=schemas.ShareOut)
def create_share(share: schemas.ShareCreate, db: Session = Depends(get_db)):
    return crud.create_share(db=db, share=share)

# 특정 공유 조회 엔드포인트
# 주어진 share_id에 해당하는 공유 정보를 반환
@app.get("/shares/{share_id}", response_model=schemas.ShareOut)
def read_share(share_id: int, db: Session = Depends(get_db)):
    db_share = crud.get_share(db, share_id=share_id)
    if db_share is None:
        raise HTTPException(status_code=404, detail="Share not found")
    return db_share

# 공유 삭제 엔드포인트
# 주어진 share_id에 해당하는 공유 정보를 삭제
@app.delete("/shares/{share_id}", response_model=schemas.ShareOut)
def delete_share(share_id: int, db: Session = Depends(get_db)):
    db_share = crud.delete_share(db=db, share_id=share_id)
    if db_share is None:
        raise HTTPException(status_code=404, detail="Share not found")
    return db_share
