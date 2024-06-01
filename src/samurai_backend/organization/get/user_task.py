from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from sqlmodel import func, select

from samurai_backend.db import get_db_session_object
from samurai_backend.enums.task_state import TaskState
from samurai_backend.models.user_projects.project import UserProjectModel
from samurai_backend.models.user_projects.task import UserTaskModel
from samurai_backend.models.user_projects.user_project_link import UserProjectLinkModel
from samurai_backend.organization.schemas.user_task import (
    UserTaskSearch,
    UserTaskSearchOutput,
)
from samurai_backend.schemas import PaginationMetaInformation
from samurai_backend.utils.get_count import get_count

if TYPE_CHECKING:
    import pydantic
    from sqlmodel import Session


def get_task_by_id(
    session: Session,
    task_id: pydantic.UUID4,
    account_id: pydantic.UUID4,
) -> UserTaskModel | None:
    value = session.exec(
        select(
            UserTaskModel,
        ).where(
            UserTaskModel.task_id == task_id,
            UserTaskModel.project.has(
                UserProjectModel.account_links.any(
                    UserProjectLinkModel.account_id == account_id,
                ),
            ),
        )
    ).first()

    if not value:
        return None

    return value


def search_tasks(
    session: Session,
    search_input: UserTaskSearch,
) -> UserTaskSearchOutput:
    query = select(
        UserTaskModel,
    ).order_by(
        UserTaskModel.priority.asc(),
        UserTaskModel.due_date.asc(),
        UserTaskModel.updated_at.desc(),
    )

    query = query.where(
        UserTaskModel.project.has(
            UserProjectModel.account_links.any(
                UserProjectLinkModel.account_id == search_input.account_id,
            ),
        ),
        UserTaskModel.project_id == search_input.project_id,
    )

    if search_input.name:
        query = query.where(
            UserTaskModel.name.icontains(search_input.name),
        )

    total = get_count(session, query)
    query = query.offset(search_input.offset).limit(search_input.page_size)

    rows = session.exec(query)

    return UserTaskSearchOutput(
        meta=PaginationMetaInformation(
            total=total,
            page=search_input.page,
            page_size=search_input.page_size,
        ),
        content=rows,
    )


def tasks_count_by_status(
    project_id: pydantic.UUID4,
    session: Session = None,
) -> dict[TaskState, int]:
    if session is None:
        session = get_db_session_object()

    result = defaultdict(int)

    for state in TaskState:
        result[state.value] = 0

    query = (
        select(
            UserTaskModel.state,
            func.count(UserTaskModel.state),
        )
        .where(
            UserTaskModel.project_id == project_id,
        )
        .group_by(
            UserTaskModel.state,
        )
    )

    rows = session.exec(query)

    for state, count in rows:
        result[state] = count

    return result
