from sqlalchemy.orm import Session
from models.images import Images
from models.file import File
from schemas.image_schema import ImageCreate, ImageResponse

def create_image(db: Session, image:ImageCreate):
    db_image = Images(
        image_id=image.image_id,
        file_id=image.file_id,
        file_url=image.file_url,
        model=image.model
    )

    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_images(db: Session, image_id: str):

    image_query = db.query(Images).filter(Images.image_id == image_id).all()
    
    response_models = []

    for image in image_query:
        # File 테이블에서 file_id로 파일 정보 필터링
        file_query = db.query(File).filter(File.file_id == image.file_id).first()

        if file_query:
            response_model = {
                "file_id":file_query.file_id,   # file_id로 사용 (필요한 경우)
                "file_name":file_query.file_name,      # url은 그대로 사용
                "file_url":file_query.file_url    # model에 image.name 사용
            }

            response_models.append(response_model)

    return response_models
    

