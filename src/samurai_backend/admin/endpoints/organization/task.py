from typing import Annotated

import pydantic
from fastapi import Body, Depends

from samurai_backend.admin.router import admin_router
from samurai_backend.core.operations import delete_entity, store_entity, update_entity
from samurai_backend.dependencies import database_session, database_session_type
from samurai_backend.errors import SamuraiNotFoundError
from samurai_backend.models.projects.task import CreateTask, TaskModel, TaskRepresentation
from samurai_backend.organization.get import task as task_get


@admin_router.post(
    "/task",
)
async def create_task(
    session: Annotated[database_session_type, Depends(database_session)],
    task: Annotated[CreateTask, Body()],
) -> TaskRepresentation:
    entity = TaskModel.model_validate(task, from_attributes=True)
    return TaskRepresentation.model_validate(
        store_entity(db=session, entity=entity),
        from_attributes=True,
    )


@admin_router.get(
    "/task/{task_id}",
)
async def get_task(
    session: Annotated[database_session_type, Depends(database_session)],
    task_id: pydantic.UUID4,
) -> TaskRepresentation:
    task = task_get.get_task_by_id(
        session,
        task_id,
    )
    if not task:
        raise SamuraiNotFoundError

    return TaskRepresentation.model_validate(
        task,
        from_attributes=True,
    )


@admin_router.get(
    "/tasks",
)
async def search_tasks(
    session: Annotated[database_session_type, Depends(database_session)],
    search: Annotated[task_get.TaskSearchInput, Depends()],
) -> task_get.TaskSearchOutput:
    return task_get.search_tasks(
        session=session,
        search_input=search,
    )


@admin_router.put(
    "/task/{task_id}",
)
async def update_task(
    session: Annotated[database_session_type, Depends(database_session)],
    task_id: pydantic.UUID4,
    task: Annotated[CreateTask, Body()],
) -> TaskRepresentation:
    entity = task_get.get_task_by_id(
        session,
        task_id,
    )
    if not entity:
        raise SamuraiNotFoundError

    entity = TaskModel.model_validate(task, from_attributes=True)
    entity.task_id = task_id

    return TaskRepresentation.model_validate(
        update_entity(
            session=session,
            entity=entity,
            primary_key="task_id",
        ),
        from_attributes=True,
    )


@admin_router.delete(
    "/task/{task_id}",
    status_code=204,
)
async def delete_task(
    session: Annotated[database_session_type, Depends(database_session)],
    task_id: pydantic.UUID4,
) -> None:
    entity = task_get.get_task_by_id(
        session,
        task_id,
    )
    if not entity:
        raise SamuraiNotFoundError

    delete_entity(session=session, entity=entity)
