from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


def build_engine():
    return create_engine(get_settings().database_url, pool_pre_ping=True)


def create_session_factory():
    return sessionmaker(bind=build_engine(), expire_on_commit=False)
