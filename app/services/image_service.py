from sqlalchemy.orm import Session
from models.images import Images
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