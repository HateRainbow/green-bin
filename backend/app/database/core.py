from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import env
from fastapi_utils.guid_type import setup_guids_postgresql

engine = create_engine(env.DATABASE_URL, echo=True)
setup_guids_postgresql(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
