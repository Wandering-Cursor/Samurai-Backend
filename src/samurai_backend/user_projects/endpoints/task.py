from typing import Annotated

import pydantic
from fastapi import Body, Depends

from samurai_backend.dependencies import (
    account_type,
    database_session,
    database_session_type,
    get_current_account,
)
from samurai_backend.enums import Permissions
from samurai_backend.errors import SamuraiNotFoundError
from samurai_backend.organization.get import user_task as task_get
from samurai_backend.organization.schemas.user_task import (
    UserTaskRepresentation,
    UserTaskSearch,
    UserTaskSearchInput,
    UserTaskSearchOutput,
    UserTaskStatusUpdateInput,
)
from samurai_backend.user_projects.operations import task as task_operations
from samurai_backend.user_projects.router import user_projects_router


@user_projects_router.get(
    "/tasks/{project_id}",
    dependencies=[
        Permissions.TASKS_READ.as_security,
    ],
    tags=["student"],
)
async def get_project_tasks(
    project_id: pydantic.UUID4,
    search_input: Annotated[UserTaskSearchInput, Depends()],
    session: Annotated[database_session_type, Depends(database_session)],
    account: Annotated[account_type, Depends(get_current_account)],
) -> UserTaskSearchOutput:
    return task_get.search_tasks(
        session,
        UserTaskSearch(
            account_id=account.account_id,
            project_id=project_id,
            **search_input.model_dump(),
        ),
    )


@user_projects_router.get(
    "/task/{task_id}",
    dependencies=[
        Permissions.TASKS_READ.as_security,
    ],
    tags=["student"],
)
async def get_task(
    task_id: pydantic.UUID4,
    session: Annotated[database_session_type, Depends(database_session)],
    account: Annotated[account_type, Depends(get_current_account)],
) -> UserTaskRepresentation:
    task_entity = task_get.get_task_by_id(
        session=session,
        task_id=task_id,
        account_id=account.account_id,
    )

    if task_entity is None:
        raise SamuraiNotFoundError

    return UserTaskRepresentation.model_validate(
        task_entity,
        from_attributes=True,
    )


@user_projects_router.put(
    "/task/{task_id}/status",
    dependencies=[
        Permissions.TASKS_UPDATE.as_security,
    ],
    tags=["student"],
)
async def update_task_status(
    task_id: pydantic.UUID4,
    update: Annotated[UserTaskStatusUpdateInput, Body()],
    session: Annotated[database_session_type, Depends(database_session)],
    account: Annotated[account_type, Depends(get_current_account)],
) -> UserTaskRepresentation:
    task_entity = task_get.get_task_by_id(
        session=session,
        task_id=task_id,
        account_id=account.account_id,
    )

    if task_entity is None:
        raise SamuraiNotFoundError

    task_entity = task_operations.update_task_state(
        session=session,
        task_id=task_id,
        update=update,
        updater=account,
    )

    return UserTaskRepresentation.model_validate(
        task_entity,
        from_attributes=True,
    )


@user_projects_router.put(
    "/task/{task_id}",
    dependencies=[
        Permissions.TASKS_EDITOR_UPDATE.as_security,
    ],
)
async def update_task(
    task_id: pydantic.UUID4,
    update: Annotated[UserTaskRepresentation, Body()],
    session: Annotated[database_session_type, Depends(database_session)],
    account: Annotated[account_type, Depends(get_current_account)],
) -> UserTaskRepresentation:
    task_entity = task_get.get_task_by_id(
        session=session,
        task_id=task_id,
        account_id=account.account_id,
    )

    if task_entity is None:
        raise SamuraiNotFoundError

    task_entity = task_operations.update_task(
        session=session,
        old_entity=task_entity,
        update=update,
    )

    return UserTaskRepresentation.model_validate(
        task_entity,
        from_attributes=True,
    )


@user_projects_router.delete(
    "/task/{task_id}",
    dependencies=[
        Permissions.TASKS_EDITOR_DELETE.as_security,
    ],
    status_code=204,
)
async def delete_task(
    task_id: pydantic.UUID4,
    session: Annotated[database_session_type, Depends(database_session)],
    account: Annotated[account_type, Depends(get_current_account)],
) -> None:
    task_entity = task_get.get_task_by_id(
        session=session,
        task_id=task_id,
        account_id=account.account_id,
    )

    if task_entity is None:
        raise SamuraiNotFoundError

    return task_operations.delete_task(
        session=session,
        task=task_entity,
    )


@user_projects_router.post(
    "/task",
    dependencies=[
        Permissions.TASKS_EDITOR_CREATE.as_security,
    ],
)
async def create_task(
    task: Annotated[UserTaskRepresentation, Body()],
    session: Annotated[database_session_type, Depends(database_session)],
) -> UserTaskRepresentation:
    task_entity = task_operations.create_task(
        session=session,
        task=task,
    )

    return UserTaskRepresentation.model_validate(
        task_entity,
        from_attributes=True,
    )
