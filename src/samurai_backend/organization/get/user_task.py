from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.core.schemas import PaginationMetaInformation
from samurai_backend.models.user_projects.project import UserProjectModel
from samurai_backend.models.user_projects.task import UserTaskModel
from samurai_backend.models.user_projects.user_project_link import UserProjectLinkModel
from samurai_backend.organization.schemas.user_task import (
    UserTaskSearch,
    UserTaskSearchOutput,
)
from samurai_backend.utils import get_count

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
        )
    ).first()

    if not value:
        return None

    project: UserProjectModel = value.project
    if not any(account_link.account_id == account_id for account_link in project.account_links):
        return None

    return value


def search_tasks(
    session: Session,
    search_input: UserTaskSearch,
) -> UserTaskSearchOutput:
    query = select(
        UserTaskModel,
    )

    query = query.where(
        UserTaskModel.project.has(
            UserProjectModel.account_links.any(
                UserProjectLinkModel.account_id == search_input.account_id,
            ),
        ),
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