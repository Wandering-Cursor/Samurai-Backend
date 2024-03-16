import pydantic
from sqlmodel import Session, SQLModel

from samurai_backend.admin.get.connections import get_connection


def add_connections(db: Session, entity: SQLModel, connections: list[pydantic.UUID4]) -> SQLModel:
    entity.connections = [
        get_connection(
            db=db,
            connection_id=connection_id,
        )
        for connection_id in connections
    ]
    return entity
