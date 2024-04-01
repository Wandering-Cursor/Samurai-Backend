from typing import Annotated

from fastapi import Depends

from samurai_backend.dependencies import (
    account_type,
    database_session,
    database_session_type,
    get_current_account,
)
from samurai_backend.errors import SamuraiNotFoundError
from samurai_backend.organization.get import user_task as task_get
from samurai_backend.organization.schemas.user_task import (
    UserTaskRepresentation,
    UserTaskSearch,
    UserTaskSearchInput,
    UserTaskSearchOutput,
)
from samurai_backend.user_projects.router import tasks_read, user_projects_router


@user_projects_router.get(
    "/tasks/{project_id}",
    dependencies=[
        tasks_read,
    ],
)
async def get_project_tasks(
    project_id: str,
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
        tasks_read,
    ],
)
async def get_task(
    task_id: str,
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
