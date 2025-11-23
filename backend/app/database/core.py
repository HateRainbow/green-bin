from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config import env
from typing import Annotated
from fastapi import Depends


engine = create_engine(env.DATABASE_URL, echo=True)


# Setup pgcrypto extension for UUID support (SQLAlchemy 2.0+ compatible)
# Note: This is deferred - will run when the app starts, not at import time
def setup_database():
    """Call this once when your app starts to setup extensions"""
    with engine.connect() as conn:
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS "pgcrypto"'))
        conn.commit()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
