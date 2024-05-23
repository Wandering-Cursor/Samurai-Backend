from typing import Annotated

import pydantic
from fastapi import BackgroundTasks, Body, Depends
from sqlmodel import Session as DatabaseSessionType

from samurai_backend.admin.router import admin_router
from samurai_backend.admin.schemas.project import BatchCreateProject
from samurai_backend.core.operations import delete_entity, store_entity, update_entity
from samurai_backend.db import get_db_session_async
from samurai_backend.errors import SamuraiNotFoundError
from samurai_backend.models.projects.project import (
    CreateProject,
    ProjectModel,
    ProjectRepresentation,
    ProjectRepresentationFull,
)
from samurai_backend.organization.get import project as project_get
from samurai_backend.organization.operations import project as project_operations
from samurai_backend.organization.schemas import project as project_schemas


@admin_router.post(
    "/project",
)
async def create_project(
    session: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
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
    session: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
    project_id: pydantic.UUID4,
) -> ProjectRepresentationFull:
    project = project_get.get_project_by_id(
        session,
        project_id,
    )
    if not project:
        raise SamuraiNotFoundError

    return ProjectRepresentationFull.model_validate(
        project,
        from_attributes=True,
    )


@admin_router.get(
    "/projects",
)
async def search_projects(
    session: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
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
    session: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
    project_id: pydantic.UUID4,
    project: Annotated[CreateProject, Body()],
) -> ProjectRepresentationFull:
    entity = ProjectModel.model_validate(project, from_attributes=True)
    entity.project_id = project_id

    return ProjectRepresentationFull.model_validate(
        update_entity(
            session=session,
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
    session: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
    project_id: pydantic.UUID4,
) -> None:
    project = project_get.get_project_by_id(
        session,
        project_id,
    )
    if not project:
        raise SamuraiNotFoundError

    delete_entity(
        session=session,
        entity=project,
    )


@admin_router.post(
    "/project/{project_id}/assign",
)
async def assign_project(
    session: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
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


@admin_router.post(
    "/project/batch",
)
async def batch_create_projects(
    session: Annotated[DatabaseSessionType, Depends(get_db_session_async)],
    projects: Annotated[list[BatchCreateProject], Body()],
    background_tasks: Annotated[BackgroundTasks, BackgroundTasks()],
) -> str:
    for project in projects:
        background_tasks.add_task(
            project_operations.create_project_from_batch,
            session=session,
            template=project,
        )

    return "ok"
