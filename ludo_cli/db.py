import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Load environment variables from .env file
load_dotenv()

class Base(DeclarativeBase):
    pass


def get_engine(db_url: str | None = None):
    url = db_url or os.getenv("DATABASE_URL", "sqlite:///ludo.db")
    return create_engine(url, echo=False, future=True)


def get_session_factory(db_url: str | None = None):
    engine = get_engine(db_url)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

