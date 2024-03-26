from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.core.schemas import PaginationMetaInformation
from samurai_backend.models.organization.group import GroupModel
from samurai_backend.organization.schemas.group import GroupSearchInput, GroupSearchOutput
from samurai_backend.utils import get_count

if TYPE_CHECKING:
    import pydantic
    from sqlmodel import Session


def get_group_by_id(
    session: Session,
    group_id: pydantic.UUID4,
) -> GroupModel | None:
    return session.exec(
        select(
            GroupModel,
        ).where(
            GroupModel.group_id == group_id,
        )
    ).first()


def get_group_search(
    session: Session,
    search: GroupSearchInput,
) -> GroupSearchOutput:
    query = select(
        GroupModel,
    )

    if search.faculty_id:
        query = query.filter(
            GroupModel.faculty_id == search.faculty_id,
        )

    if search.name:
        query = query.filter(
            GroupModel.name.icontains(search.name),
        )

    total = get_count(session, query)
    query = query.offset(search.search_page * search.page_size).limit(search.page_size)

    rows = session.exec(query)

    return GroupSearchOutput(
        content=rows.all(),
        meta=PaginationMetaInformation(
            total=total,
            page=search.page,
            page_size=search.page_size,
        ),
    )
