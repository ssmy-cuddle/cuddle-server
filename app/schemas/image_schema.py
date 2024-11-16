from pydantic import BaseModel, Field
from typing import Optional

class ImageBase(BaseModel):
    image_id: str
    file_id: str
    file_url: str = Field(..., description="URL of the file on S3")

class ImageCreate(BaseModel):
    image_id: str
    file_id: str
    file_url: Optional[str]
    model: Optional[str]

class ImageResponse(BaseModel):
    image_id: str
    file_id: str
    file_url: str = Field(..., description="URL of the file on S3")
    model: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True  # ORM 객체에서 속성 매핑 가능하게 설정
