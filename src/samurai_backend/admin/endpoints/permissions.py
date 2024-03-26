from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends

from samurai_backend.admin.get import permissions as permissions_get
from samurai_backend.admin.router import admin_router
from samurai_backend.core.operations import store_entity
from samurai_backend.dependencies import database_session, database_session_type
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
    db: Annotated[database_session_type, Depends(database_session)],
) -> Sequence[AccountPermission]:
    return permissions_get.get_permissions(db=db)


@admin_router.post(
    "/permissions",
    description="Create a permission.",
)
async def create_permission(
    db: Annotated[database_session_type, Depends(database_session)],
    permission: CreatePermission,
) -> PermissionBase:
    return PermissionBase.model_validate(
        store_entity(
            db=db,
            entity=AccountPermission(**permission.model_dump()),
        ),
        from_attributes=True,
    )
