from typing import Annotated

import pydantic
from fastapi import Body, Depends
from sqlmodel import Session

from samurai_backend.db import get_db_session_async
from samurai_backend.dependencies.get_current_active_account import get_current_active_account
from samurai_backend.enums.account_type import AccountType as AccountTypeEnum
from samurai_backend.enums.permissions import Permissions
from samurai_backend.errors import SamuraiInvalidRequestError, SamuraiNotFoundError
from samurai_backend.models.account.account import AccountModel
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
    session: Annotated[Session, Depends(get_db_session_async)],
    search: Annotated[ProjectSearchInput, Depends()],
    account: Annotated[AccountModel, Depends(get_current_active_account)],
) -> UserProjectSearchOutput:
    """
    Get all available projects by specifying the search criteria.
    """
    if search.account_id and account.account_type == AccountTypeEnum.STUDENT:
        raise SamuraiInvalidRequestError(
            detail_override="You are not allowed to search by account_id.",
        )

    # This is done so admins can see all projects.
    account_id = None
    if search.account_id:
        account_id = search.account_id
    if account.account_type != AccountTypeEnum.ADMIN:
        account_id = account.account_id

    return project_get.search_projects(
        session=session,
        search_input=search,
        related_account_id=account_id,
    )


@user_projects_router.get(
    "/projects/current",
    dependencies=[
        Permissions.PROJECTS_READ.as_security,
    ],
    tags=["student"],
)
async def get_current_projects(
    session: Annotated[Session, Depends(get_db_session_async)],
    account: Annotated[AccountModel, Depends(get_current_active_account)],
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
    session: Annotated[Session, Depends(get_db_session_async)],
    project_id: pydantic.UUID4,
    account: Annotated[AccountModel, Depends(get_current_active_account)],
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
    session: Annotated[Session, Depends(get_db_session_async)],
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
        Permissions.ADMIN.as_security,
    ],
)
async def delete_project(
    session: Annotated[Session, Depends(get_db_session_async)],
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
