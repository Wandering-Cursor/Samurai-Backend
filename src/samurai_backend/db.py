from collections.abc import AsyncGenerator

from sqlmodel import Session, SQLModel, create_engine

from samurai_backend import models
from samurai_backend.settings import settings

__all__ = [
    "models",
]

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)


async def get_db_session() -> AsyncGenerator[Session, None, None]:
    """
    Returns a generator that yields a database session.
    """
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


def create_all_tables() -> None:
    SQLModel.metadata.create_all(engine)
