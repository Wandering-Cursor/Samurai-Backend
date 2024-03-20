from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.core.schemas import PaginationMetaInformation
from samurai_backend.models.organization.department import DepartmentModel
from samurai_backend.organization.schemas.department import (
    DepartmentSearchInput,
    DepartmentSearchOutput,
)
from samurai_backend.utils import get_count

if TYPE_CHECKING:
    from sqlmodel import Session


def get_department_by_id(
    session: Session,
    department_id: str,
) -> DepartmentModel | None:
    """
    Get a department by its ID
    """
    return session.exec(
        select(
            DepartmentModel,
        ).where(
            DepartmentModel.department_id == department_id,
        )
    ).first()


def get_departments_search(
    session: Session,
    search: DepartmentSearchInput,
) -> DepartmentSearchOutput:
    """
    Search for departments
    """
    query = select(
        DepartmentModel,
    )

    if search.name:
        query = query.filter(
            DepartmentModel.name.icontains(search.name),
        )

    total = get_count(session, query)
    query = query.offset(search.search_page * search.page_size).limit(search.page_size)

    rows = session.exec(query)

    return DepartmentSearchOutput(
        content=rows.all(),
        meta=PaginationMetaInformation(
            total=total,
            page=search.page,
            page_size=search.page_size,
        ),
    )