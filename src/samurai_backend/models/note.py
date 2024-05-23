from collections.abc import Generator

import sqlmodel
from baas_auth.models.base import BaseModel
from baas_auth.settings import settings_instance
from baas_auth.utils.current_time import get_current_time
from sqlalchemy import event
from sqlmodel.main import default_registry

engine = sqlmodel.create_engine(
    url=settings_instance.rdms_connection_string,
)


def create_db_and_tables() -> None:
    sqlmodel.SQLModel.metadata.create_all(engine)


def update_timestamp_before_update(mapper, connection, target: BaseModel) -> None:  # noqa: ANN001, ARG001
    if hasattr(target, "updated_at"):
        target.updated_at = get_current_time()


create_db_and_tables()

for mapper in default_registry.mappers:
    if BaseModel in mapper.class_.__mro__:
        event.listen(
            mapper,
            "before_update",
            update_timestamp_before_update,
        )


def get_session() -> sqlmodel.Session:
    return sqlmodel.Session(engine)


def session_generator() -> Generator[sqlmodel.Session, None, None]:
    session = get_session()
    try:
        yield session
    finally:
        session.close()
