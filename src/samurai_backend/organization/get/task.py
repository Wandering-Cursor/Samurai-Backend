from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.models.projects.task import TaskModel
from samurai_backend.organization.schemas.task import TaskSearchInput, TaskSearchOutput
from samurai_backend.schemas import PaginationMetaInformation
from samurai_backend.utils.get_count import get_count

if TYPE_CHECKING:
    import pydantic
    from sqlmodel import Session


def get_task_by_id(
    session: Session,
    task_id: pydantic.UUID4,
) -> TaskModel | None:
    return session.exec(
        select(
            TaskModel,
        ).where(
            TaskModel.task_id == task_id,
        )
    ).first()


def search_tasks(
    session: Session,
    search_input: TaskSearchInput,
) -> TaskSearchOutput:
    query = select(
        TaskModel,
    ).order_by(
        TaskModel.priority.asc(),
        TaskModel.due_date.asc(),
        TaskModel.updated_at.desc(),
    )

    if search_input.project_id:
        query = query.where(
            TaskModel.project_id == search_input.project_id,
        )
    if search_input.name:
        query = query.where(
            TaskModel.name.icontains(search_input.name),
        )

    total = get_count(session, query)
    query = query.offset(search_input.offset).limit(search_input.page_size)

    rows = session.exec(query)

    return TaskSearchOutput(
        meta=PaginationMetaInformation(
            total=total,
            page=search_input.page,
            page_size=search_input.page_size,
        ),
        content=list(rows.all()),
    )
