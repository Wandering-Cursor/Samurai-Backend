from typing import Annotated

from fastapi import Depends
from sqlmodel import Session as DatabaseSessionType

from samurai_backend.admin.get import permissions as permissions_get
from samurai_backend.admin.router import admin_router
from samurai_backend.core.operations import store_entity
from samurai_backend.db import get_db_session_async
from samurai_backend.models.account.account_permission import (
    AccountPermission,
    CreatePermission,
    PermissionBase,
)


@admin_router.get(
    "/permissions",
    description="Get all permissions.",
)
async def get_permissions(
    db: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
) -> list[AccountPermission]:
    return permissions_get.get_permissions(db=db)


@admin_router.post(
    "/permissions",
    description="Create a permission.",
)
async def create_permission(
    db: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
    permission: CreatePermission,
) -> PermissionBase:
    return PermissionBase.model_validate(
        store_entity(
            db=db,
            entity=AccountPermission(**permission.model_dump()),
        ),
        from_attributes=True,
    )
