from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from samurai_backend.db import get_db_session_async
from samurai_backend.enums.permissions import Permissions
from samurai_backend.errors import SamuraiInvalidRequestError
from samurai_backend.models.account.account import AccountModel
from samurai_backend.organization.get import user_project as project_get
from samurai_backend.organization.schemas import user_project as user_project_schemas
from samurai_backend.user_projects.router import stats_projects_router


@stats_projects_router.get(
    "/teachers",
)
async def get_stats_per_teacher(
    session: Annotated[Session, Depends(get_db_session_async)],
    account: Annotated[AccountModel, Permissions.PROJECTS_STATS.as_security],
) -> user_project_schemas.ProjectsStatsByTeacher:
    faculty_id = None

    for connection in account.connections:
        if connection.faculty_id:
            faculty_id = connection.faculty_id
            break

    if not faculty_id:
        raise SamuraiInvalidRequestError("You do not have connection to any faculty.")

    return project_get.get_projects_stats_by_teacher(
        session=session,
        faculty_id=faculty_id,
    )


@stats_projects_router.get(
    "/tasks",
)
async def get_stats_by_tasks(
    session: Annotated[Session, Depends(get_db_session_async)],
    account: Annotated[AccountModel, Permissions.PROJECTS_STATS.as_security],
    query: Annotated[user_project_schemas.ProjectsStatsByTaskInput, Depends()],
) -> user_project_schemas.ProjectsStatsByTask:
    faculty_id = None

    for connection in account.connections:
        if connection.faculty_id:
            faculty_id = connection.faculty_id
            break

    if not faculty_id:
        raise SamuraiInvalidRequestError("You do not have connection to any faculty.")

    return project_get.get_projects_stats_by_task(
        session=session,
        faculty_id=faculty_id,
        query=query,
    )
