from collections.abc import AsyncGenerator, Generator

from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine

from samurai_backend import models
from samurai_backend.settings import settings

__all__ = [
    "models",
]

SQLALCHEMY_DATABASE_URL = settings.database_url


def make_engine() -> Engine:
    return create_engine(SQLALCHEMY_DATABASE_URL)


engine = make_engine()


def get_db_session() -> Generator[Session, None, None]:
    """
    Returns a database session.
    """
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


async def get_db_session_async() -> AsyncGenerator[Session, None]:
    """
    Returns a generator that yields a database session.
    """
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
