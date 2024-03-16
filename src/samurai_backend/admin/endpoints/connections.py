from typing import Annotated

from fastapi import Depends

from samurai_backend.admin.get import connections as connections_get
from samurai_backend.admin.router import admin_router
from samurai_backend.core.operations import store_entity
from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.models.account.connection import ConnectionBase, ConnectionModel


@admin_router.get(
    "/connections",
    description="Get all connections.",
)
async def get_connections(
    db: Annotated[database_session_type, Depends(database_session)],
) -> list[ConnectionBase]:
    return connections_get.get_connections(db=db)


@admin_router.post(
    "/connections",
    description="Create a permission.",
)
async def create_connection(
    db: Annotated[database_session_type, Depends(database_session)],
    connection: ConnectionBase,
) -> ConnectionBase:
    value = store_entity(db=db, entity=ConnectionModel(**connection.model_dump()))
    return value  # noqa: RET504
