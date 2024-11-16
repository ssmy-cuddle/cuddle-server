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
    image_query = db.query(Images)
    image_query = image_query.filter(Images.image_id == image_id)
    
    response_models = []

    for file_id in image_query:
        file_query = db.query(File)
        file_query = file_query.filter(File.file_id == file_id)

        response_model = {
            "file_id":file_query.file_id,   # file_id로 사용 (필요한 경우)
            "file_name":file_query.file_name,      # url은 그대로 사용
            "file_url":file_query.file_url    # model에 image.name 사용
        }

        response_models.append(response_model)

    return response_models
    

