from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.models.account.connection import ConnectionModel

if TYPE_CHECKING:
    from collections.abc import Sequence

    import pydantic
    from sqlmodel import Session


def get_connections(
    db: Session,
) -> Sequence[ConnectionModel]:
    query = select(ConnectionModel)
    return db.exec(query).all()


def get_connection(
    db: Session,
    connection_id: pydantic.UUID4,
) -> ConnectionModel | None:
    query = select(ConnectionModel).filter(
        ConnectionModel.connection_id == connection_id,
    )
    return db.exec(query).first()
