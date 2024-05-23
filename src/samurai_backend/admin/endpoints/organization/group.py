from typing import Annotated

from fastapi import Body, Depends
from sqlmodel import Session as DatabaseSessionType

from samurai_backend.admin.router import admin_router
from samurai_backend.core.operations import delete_entity, store_entity, update_entity
from samurai_backend.db import get_db_session_async
from samurai_backend.models.organization.group import Group, GroupCreate, GroupModel
from samurai_backend.organization.dependencies import group_exists
from samurai_backend.organization.get.group import get_group_search
from samurai_backend.organization.schemas.group import GroupSearchInput, GroupSearchOutput


@admin_router.get(
    "/group",
)
async def get_groups(
    session: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
    search: Annotated[GroupSearchInput, Depends()],
) -> GroupSearchOutput:
    """Returns a list of groups found by the search parameters."""
    return get_group_search(
        session=session,
        search=search,
    )


@admin_router.get(
    "/group/{group_id}",
)
async def get_group(
    group: Annotated[GroupModel, Depends(group_exists)],
) -> Group:
    """Returns a group by its ID."""
    return Group.model_validate(group, from_attributes=True)


@admin_router.post(
    "/group",
)
async def create_group(
    session: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
    body: Annotated[GroupCreate, Body(...)],
) -> Group:
    """Creates a new group."""
    group_model = GroupModel.model_validate(body)
    store_entity(session, group_model)
    return Group.model_validate(group_model, from_attributes=True)


@admin_router.put(
    "/group/{group_id}",
)
async def update_group(
    session: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
    body: Annotated[GroupCreate, Body(...)],
    original_group: Annotated[GroupModel, Depends(group_exists)],
) -> Group:
    """Updates a group."""
    group = GroupModel.model_validate(body)
    group.group_id = original_group.group_id

    updated_group = update_entity(session, group, "group_id")
    return Group.model_validate(updated_group, from_attributes=True)


@admin_router.delete(
    "/group/{group_id}",
    status_code=204,
)
async def delete_group(
    session: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
    group: Annotated[GroupModel, Depends(group_exists)],
) -> None:
    delete_entity(
        session=session,
        entity=group,
    )
