from typing import Annotated

import pydantic
from fastapi import Body, Depends

from samurai_backend.dependencies import (
    account_type,
    database_session,
    database_session_type,
    get_current_active_account,
)
from samurai_backend.enums import AccountType, Permissions
from samurai_backend.errors import SamuraiInvalidRequestError, SamuraiNotFoundError
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
    tags=["student"],
)
async def get_projects(
    session: Annotated[database_session_type, Depends(database_session)],
    search: Annotated[ProjectSearchInput, Depends()],
    account: Annotated[account_type, Depends(get_current_active_account)],
) -> UserProjectSearchOutput:
    """
    Get all available projects by specifying the search criteria.
    """
    if search.account_id and account.account_type == AccountType.STUDENT:
        raise SamuraiInvalidRequestError(
            detail_override="You are not allowed to search by account_id.",
        )

    return project_get.search_projects(
        session=session,
        search_input=search,
        related_account_id=search.account_id or account.account_id,
    )


@user_projects_router.get(
    "/projects/current",
    dependencies=[
        Permissions.PROJECTS_READ.as_security,
    ],
    tags=["student"],
)
async def get_current_projects(
    session: Annotated[database_session_type, Depends(database_session)],
    account: Annotated[account_type, Depends(get_current_active_account)],
) -> UserProjectRepresentation:
    """
    Get all available projects linked to the student.
    """
    project = project_get.get_last_linked_project(
        session=session,
        account_id=account.account_id,
    )
    if not project:
        raise SamuraiNotFoundError(
            detail_override="You do not have an assigned project.",
        )

    return UserProjectRepresentation.model_validate(
        project,
        from_attributes=True,
    )


@user_projects_router.get(
    "/projects/{project_id}",
    dependencies=[
        Permissions.PROJECTS_READ.as_security,
    ],
    tags=["student"],
)
async def get_project(
    session: Annotated[database_session_type, Depends(database_session)],
    project_id: pydantic.UUID4,
    account: Annotated[account_type, Depends(get_current_active_account)],
) -> UserProjectRepresentation:
    """
    Get a specific project (if it's linked to you).
    """
    project = project_get.get_linked_project_by_id(
        session=session,
        project_id=project_id,
        account_id=account.account_id,
    )
    if not project:
        raise SamuraiNotFoundError

    return UserProjectRepresentation.model_validate(
        project,
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


@user_projects_router.delete(
    "/projects/{project_id}",
    dependencies=[
        Permissions.PROJECTS_DELETE.as_security,
    ],
)
async def delete_project(
    session: Annotated[database_session_type, Depends(database_session)],
    project_id: pydantic.UUID4,
) -> dict[str, str]:
    """
    Delete a project.
    """
    project = project_get.get_project_by_id(
        session=session,
        project_id=project_id,
    )
    if not project:
        raise SamuraiNotFoundError

    project_operations.delete_project(
        session=session,
        project=project,
    )

    return {"message": "Project deleted."}
