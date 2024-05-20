from typing import Annotated

from fastapi import Depends

from samurai_backend.dependencies import account_type, database_session, database_session_type
from samurai_backend.enums import Permissions
from samurai_backend.errors import SamuraiInvalidRequestError
from samurai_backend.organization.get import user_project as project_get
from samurai_backend.organization.schemas import user_project as user_project_schemas
from samurai_backend.user_projects.router import stats_projects_router


@stats_projects_router.get(
    "/stats/teachers",
)
async def get_stats_per_teacher(
    session: Annotated[database_session_type, Depends(database_session)],
    account: Annotated[account_type, Permissions.PROJECTS_STATS.as_security],
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
