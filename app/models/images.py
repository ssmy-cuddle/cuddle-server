from sqlalchemy import Column, String, Text

from . import Base

class Images(Base):
    __tablename__ = "images"

    image_id = Column(String(200), primary_key=True)
    file_id = Column(String(200), primary_key=True)
    file_url = Column(Text, nullable=False)
    model = Column(String(30))