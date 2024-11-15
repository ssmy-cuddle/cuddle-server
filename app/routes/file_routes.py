# routes/file_routes.py

import hashlib
import random
import string
from fastapi import APIRouter, UploadFile, File as FastAPIFile, HTTPException, Depends
from sqlalchemy.orm import Session
from services.s3_service import upload_file_to_s3
from db.session import get_db
from models.file import File  # 올바른 File 모델 임포트
from schemas.file_schema import FileCreate

router = APIRouter()

def generate_hashed_filename(original_filename: str) -> str:
    if not isinstance(original_filename, str):
        raise ValueError("The original filename must be a string.")

    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    hash_object = hashlib.sha256(f"{original_filename}_{random_suffix}".encode())
    return hash_object.hexdigest()

@router.post("/upload")
async def upload_file(uid: str, file: UploadFile = FastAPIFile(...), db: Session = Depends(get_db)):
    # try:
        # 파일 유효성 체크
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="File must have a valid filename")

        # 파일 폴더 해시화
        hashed_dir = generate_hashed_filename(file.filename)
        if not hashed_dir:
            raise HTTPException(status_code=500, detail="Failed to generate hashed directory for file")

        s3_filename = f"uploads/{hashed_dir}/{file.filename}"

        # S3에 파일 업로드
        file_url = upload_file_to_s3(file, s3_filename)

        # 데이터베이스에 파일 정보 저장
        file_record = FileCreate(
            file_name=file.filename,
            file_url=file_url,
            uid=uid
        )
        new_file = File(**file_record.dict())
        db.add(new_file)
        db.commit()
        db.refresh(new_file)

        return {"file_id": new_file.file_id, "file_url": file_url}
    # except ValueError as ve:
    #     raise HTTPException(status_code=400, detail=str(ve))
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))