from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.models.account.connection import ConnectionModel

if TYPE_CHECKING:
    from sqlmodel import Session


def get_connections(
    db: Session,
) -> list[ConnectionModel]:
    query = select(ConnectionModel)
    return db.exec(query).all()


def get_connection(
    db: Session,
    connection_id: str,
) -> ConnectionModel | None:
    query = select(ConnectionModel).filter(
        ConnectionModel.connection_id == connection_id,
    )
    return db.exec(query).first()
