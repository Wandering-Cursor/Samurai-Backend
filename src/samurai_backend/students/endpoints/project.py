from typing import Annotated

from fastapi import Depends

from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.organization.get import user_project as project_get
from samurai_backend.organization.schemas.user_project import (
    ProjectSearchInput,
    ProjectSearchOutput,
)
from samurai_backend.students.router import student_router


@student_router.get(
    "/projects",
)
async def get_projects(
    session: Annotated[database_session_type, Depends(database_session)],
    search: Annotated[ProjectSearchInput, Depends()],
) -> ProjectSearchOutput:
    """
    Get all available projects for the student.
    """
    return project_get.search_projects(
        session=session,
        search_input=search,
    )
