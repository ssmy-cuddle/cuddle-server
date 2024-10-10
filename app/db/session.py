from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

print(settings.DATABASE_URL)

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
