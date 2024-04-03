from typing import Annotated

import pydantic
from fastapi import Body, Depends

from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.enums import Permissions
from samurai_backend.models.user_projects.project import CreateUserProject, UserProjectModel
from samurai_backend.organization.get import user_project as project_get
from samurai_backend.organization.schemas.user_project import (
    ProjectSearchInput,
    UserProjectRepresentation,
    UserProjectSearchOutput,
)
from samurai_backend.user_projects.operations import project as project_operations
from samurai_backend.user_projects.router import user_projects_router


@user_projects_router.get(
    "/projects",
    dependencies=[
        Permissions.PROJECTS_READ.as_security,
    ],
)
async def get_projects(
    session: Annotated[database_session_type, Depends(database_session)],
    search: Annotated[ProjectSearchInput, Depends()],
) -> UserProjectSearchOutput:
    """
    Get all available projects by specifying the search criteria.
    """
    return project_get.search_projects(
        session=session,
        search_input=search,
    )


@user_projects_router.get(
    "/projects/{project_id}",
    dependencies=[
        Permissions.PROJECTS_READ.as_security,
    ],
)
async def get_project(
    session: Annotated[database_session_type, Depends(database_session)],
    project_id: pydantic.UUID4,
) -> UserProjectRepresentation:
    """
    Get a specific project for the student.
    """
    return UserProjectRepresentation.model_validate(
        project_get.get_project_by_id(
            session=session,
            project_id=project_id,
        ),
        from_attributes=True,
    )


@user_projects_router.post(
    "/projects",
    dependencies=[
        Permissions.PROJECTS_CREATE.as_security,
    ],
)
async def create_project(
    session: Annotated[database_session_type, Depends(database_session)],
    project: Annotated[CreateUserProject, Body()],
) -> UserProjectRepresentation:
    """
    Create a new project for the student.
    """
    project_entity = UserProjectModel.model_validate(
        project.model_dump(exclude={"account_links"}),
    )

    session.add(project_entity)
    session.commit()

    project_entity = project_operations.assign_to_accounts(
        session=session,
        project=project_entity,
        account_ids=project.account_links,
    )

    return UserProjectRepresentation.model_validate(
        project_entity,
        from_attributes=True,
    )
