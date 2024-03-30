from typing import Annotated

import pydantic
from fastapi import Body, Depends

from samurai_backend.admin.router import admin_router
from samurai_backend.core.operations import delete_entity, store_entity, update_entity
from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.errors import SamuraiNotFoundError
from samurai_backend.models.projects.project import (
    CreateProject,
    ProjectModel,
    ProjectRepresentation,
)
from samurai_backend.organization.get import project as project_get
from samurai_backend.organization.operations import project as project_operations
from samurai_backend.organization.schemas import project as project_schemas


@admin_router.post(
    "/project",
)
async def create_project(
    session: Annotated[database_session_type, Depends(database_session)],
    project: Annotated[CreateProject, Body()],
) -> ProjectRepresentation:
    entity = ProjectModel.model_validate(project, from_attributes=True)
    return ProjectRepresentation.model_validate(
        store_entity(db=session, entity=entity),
        from_attributes=True,
    )


@admin_router.get(
    "/project/{project_id}",
)
async def get_project(
    session: Annotated[database_session_type, Depends(database_session)],
    project_id: pydantic.UUID4,
) -> ProjectRepresentation:
    project = project_get.get_project_by_id(
        session,
        project_id,
    )
    if not project:
        raise SamuraiNotFoundError

    return ProjectRepresentation.model_validate(
        project,
        from_attributes=True,
    )


@admin_router.get(
    "/projects",
)
async def search_projects(
    session: Annotated[database_session_type, Depends(database_session)],
    search: Annotated[project_schemas.ProjectSearchInput, Depends()],
) -> project_schemas.ProjectSearchOutput:
    return project_get.search_projects(
        session,
        search,
    )


@admin_router.put(
    "/project/{project_id}",
)
async def update_project(
    session: Annotated[database_session_type, Depends(database_session)],
    project_id: pydantic.UUID4,
    project: Annotated[CreateProject, Body()],
) -> ProjectRepresentation:
    entity = ProjectModel.model_validate(project, from_attributes=True)
    entity.project_id = project_id

    return ProjectRepresentation.model_validate(
        update_entity(
            db=session,
            entity=entity,
            primary_key="project_id",
        ),
        from_attributes=True,
    )


@admin_router.delete(
    "/project/{project_id}",
    status_code=204,
)
async def delete_project(
    session: Annotated[database_session_type, Depends(database_session)],
    project_id: pydantic.UUID4,
) -> None:
    project = project_get.get_project_by_id(
        session,
        project_id,
    )
    if not project:
        raise SamuraiNotFoundError

    delete_entity(
        db=session,
        entity=project,
    )


@admin_router.post(
    "/project/{project_id}/assign",
)
async def assign_project(
    session: Annotated[database_session_type, Depends(database_session)],
    project_id: pydantic.UUID4,
    body: Annotated[project_schemas.ProjectAssignBody, Body()],
) -> project_schemas.ProjectAssignOutput:
    project = project_get.get_project_by_id(
        session,
        project_id,
    )
    if not project:
        raise SamuraiNotFoundError

    assign_input = project_schemas.ProjectAssignInput(
        project_id=project_id,
        **body.model_dump(),
    )

    return project_operations.assign_project(
        session=session,
        assign_input=assign_input,
        project=project,
    )
