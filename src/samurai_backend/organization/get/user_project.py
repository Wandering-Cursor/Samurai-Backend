from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.core.schemas import PaginationMetaInformation
from samurai_backend.models.user_projects.project import UserProjectModel
from samurai_backend.organization.schemas.user_project import (
    ProjectSearchInput,
    ProjectSearchOutput,
)
from samurai_backend.utils import get_count

if TYPE_CHECKING:
    import pydantic
    from sqlmodel import Session


def get_project_by_id(
    session: Session,
    project_id: pydantic.UUID4,
) -> UserProjectModel | None:
    return session.exec(
        select(
            UserProjectModel,
        ).where(
            UserProjectModel.project_id == project_id,
        )
    ).first()


def search_projects(
    session: Session,
    search_input: ProjectSearchInput,
) -> ProjectSearchOutput:
    query = select(
        UserProjectModel,
    )

    if search_input.faculty_id:
        query = query.where(
            UserProjectModel.faculty_id == search_input.faculty_id,
        )
    if search_input.name:
        query = query.where(
            UserProjectModel.name.icontains(search_input.name),
        )

    total = get_count(session, query)
    query = query.offset(search_input.offset).limit(search_input.page_size)

    rows = session.exec(query)

    return ProjectSearchOutput(
        meta=PaginationMetaInformation(
            total=total,
            page=search_input.page,
            page_size=search_input.page_size,
        ),
        content=list(rows.all()),
    )
