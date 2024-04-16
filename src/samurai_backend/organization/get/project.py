from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.core.schemas import PaginationMetaInformation
from samurai_backend.models.projects.project import ProjectModel
from samurai_backend.organization.schemas.project import ProjectSearchInput, ProjectSearchOutput
from samurai_backend.utils.get_count import get_count

if TYPE_CHECKING:
    import pydantic
    from sqlmodel import Session


def get_project_by_id(
    session: Session,
    project_id: pydantic.UUID4,
) -> ProjectModel | None:
    return session.exec(
        select(
            ProjectModel,
        ).where(
            ProjectModel.project_id == project_id,
        )
    ).first()


def search_projects(
    session: Session,
    search_input: ProjectSearchInput,
) -> ProjectSearchOutput:
    query = select(
        ProjectModel,
    ).order_by(
        ProjectModel.updated_at.desc(),
    )

    if search_input.faculty_id:
        query = query.where(
            ProjectModel.faculty_id == search_input.faculty_id,
        )
    if search_input.name:
        query = query.where(
            ProjectModel.name.icontains(search_input.name),
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
