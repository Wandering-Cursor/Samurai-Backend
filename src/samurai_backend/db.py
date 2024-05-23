from collections.abc import AsyncGenerator, Generator

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine
from sqlmodel.main import default_registry

from samurai_backend import models
from samurai_backend.settings import settings
from samurai_backend.utils.current_time import current_time

__all__ = [
    "models",
]

SQLALCHEMY_DATABASE_URL = settings.database_url


def make_engine() -> Engine:
    return create_engine(SQLALCHEMY_DATABASE_URL)


engine = make_engine()


def update_timestamp_before_update(_, __, target: models.base.BaseModel) -> None:  # noqa: ANN001
    if hasattr(target, "updated_at"):
        target.updated_at = current_time()


for mapper in default_registry.mappers:
    if models.base.BaseModel in mapper.class_.__mro__:
        event.listen(
            mapper,
            "before_update",
            update_timestamp_before_update,
        )


def get_db_session_object() -> Session:
    """
    Returns a database session.
    """
    return Session(engine)


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
