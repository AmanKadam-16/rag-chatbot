from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from src.smart_rag.core.config import settings


engine = create_engine(settings.DATABASE_URL, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
