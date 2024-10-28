from sqlalchemy import Column, String, Integer, Date, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.user import User

Base = declarative_base()

class Pet(Base):
    __tablename__ = "pets"

    pet_id = Column(Integer, primary_key=True, autoincrement=True)  # 반려동물 ID (pk)
    uid = Column(String(50), ForeignKey(User.uid))  # 사용자 ID (fk)
    name = Column(String(50), nullable=False)  # 반려동물 이름
    birthday = Column(Date)  # 반려동물 생일
    breed = Column(String(50))  # 반려동물 품종
    adoption_date = Column(Date)  # 입양 날짜
    separation_date = Column(Date)  # 이별 날짜
    gender = Column(String(10))  # 반려동물 성별
    neutered = Column(Boolean)  # 중성화 여부
    weight = Column(DECIMAL(5, 2))  # 반려동물 몸무게 (단위: kg)
    description = Column(String)  # 반려동물 설명