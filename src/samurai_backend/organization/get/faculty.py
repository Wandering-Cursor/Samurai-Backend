from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.core.schemas import PaginationMetaInformation
from samurai_backend.models.organization.faculty import FacultyModel, FacultyRepresentation
from samurai_backend.organization.schemas.faculty import FacultySearchInput, FacultySearchOutput
from samurai_backend.utils import get_count

if TYPE_CHECKING:
    import pydantic
    from sqlmodel import Session


def get_faculty_by_id(
    session: Session,
    faculty_id: pydantic.UUID4,
) -> FacultyModel | None:
    return session.exec(
        select(
            FacultyModel,
        ).where(
            FacultyModel.faculty_id == faculty_id,
        )
    ).first()


def get_faculty_search(
    session: Session,
    search: FacultySearchInput,
) -> FacultySearchOutput:
    query = select(
        FacultyModel,
    )

    if search.department_id:
        query = query.filter(
            FacultyModel.department_id == search.department_id,
        )

    if search.name:
        query = query.filter(
            FacultyModel.name.icontains(search.name),
        )

    total = get_count(session, query)
    query = query.offset(search.search_page * search.page_size).limit(search.page_size)

    rows = session.exec(query)

    return FacultySearchOutput(
        content=[
            FacultyRepresentation.model_validate(row, from_attributes=True) for row in rows.all()
        ],
        meta=PaginationMetaInformation(
            total=total,
            page=search.page,
            page_size=search.page_size,
        ),
    )
