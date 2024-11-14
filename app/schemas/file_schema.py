from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FileBase(BaseModel):
    file_name: str = Field(..., description="Hashed file name")
    file_url: str = Field(..., description="URL of the file on S3")

class FileCreate(FileBase):
    uid: str = Field(..., description="ID of the user who uploaded the file")

class FileResponse(FileBase):
    file_id: int = Field(..., description="Unique ID of the file")
    uid: str = Field(..., description="ID of the user who uploaded the file")
    created_at: datetime = Field(..., description="File creation timestamp")

    class Config:
        orm_mode = True
