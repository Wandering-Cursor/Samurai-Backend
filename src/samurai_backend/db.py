from collections.abc import AsyncGenerator

from sqlmodel import Session, create_engine

from samurai_backend import models
from samurai_backend.settings import settings

__all__ = [
    "models",
]

SQLALCHEMY_DATABASE_URL = settings.database_url


def make_engine() -> None:
    return create_engine(SQLALCHEMY_DATABASE_URL)


engine = make_engine()


async def get_db_session() -> AsyncGenerator[Session, None, None]:
    """
    Returns a generator that yields a database session.
    """
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
