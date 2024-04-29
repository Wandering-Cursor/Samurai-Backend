from typing import Annotated

from fastapi import Depends

from samurai_backend.admin.get import connections as connections_get
from samurai_backend.admin.router import admin_router
from samurai_backend.admin.schemas import connections as connections_schemas
from samurai_backend.core.operations import store_entity
from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.models.account.connection import (
    ConnectionBase,
    ConnectionCreate,
    ConnectionModel,
)


@admin_router.get(
    "/connections",
)
async def get_connections(
    db: Annotated[database_session_type, Depends(database_session)],
    search: Annotated[connections_schemas.ConnectionsFilter, Depends()],
) -> connections_schemas.ConnectionsPaginatedResponse:
    "Execute a search among connections"
    return await connections_get.get_connections(
        session=db,
        search=search,
    )


@admin_router.post(
    "/connections",
)
async def create_connection(
    db: Annotated[database_session_type, Depends(database_session)],
    connection: ConnectionCreate,
) -> ConnectionBase:
    """Create a new connection"""

    return ConnectionBase.model_validate(
        store_entity(
            db=db,
            entity=ConnectionModel.model_validate(connection, from_attributes=True),
        ),
        from_attributes=True,
    )
