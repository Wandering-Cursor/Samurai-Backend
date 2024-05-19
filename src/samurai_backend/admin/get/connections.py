from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.admin.schemas.connections import ConnectionsPaginatedResponse
from samurai_backend.models.account.connection import ConnectionModel
from samurai_backend.utils.get_count import get_count

if TYPE_CHECKING:
    import pydantic
    from sqlmodel import Session

    from samurai_backend.admin.schemas.connections import ConnectionsFilter


async def get_connections(
    session: Session,
    search: ConnectionsFilter,
) -> ConnectionsPaginatedResponse:
    query = select(ConnectionModel).order_by(
        ConnectionModel.updated_at.desc(),
    )

    if search.connection_id:
        query = query.filter(
            ConnectionModel.connection_id == search.connection_id,
        )
    if search.group_id:
        query = query.filter(
            ConnectionModel.group_id == search.group_id,
        )
    if search.faculty_id:
        query = query.filter(
            ConnectionModel.faculty_id == search.faculty_id,
        )
    if search.department_id:
        query = query.filter(
            ConnectionModel.department_id == search.department_id,
        )

    total = get_count(session, query)
    query = query.offset(search.offset).limit(search.page_size)
    content = session.exec(query)

    return ConnectionsPaginatedResponse(
        meta=ConnectionsPaginatedResponse.construct_meta(
            total=total,
            page=search.page,
            page_size=search.page_size,
        ),
        content=content,
    )


def get_connection(
    session: Session,
    connection_id: pydantic.UUID4,
) -> ConnectionModel | None:
    query = select(ConnectionModel).filter(
        ConnectionModel.connection_id == connection_id,
    )
    return session.exec(query).first()


def get_connection_by_parameters(
    session: Session,
    group_id: pydantic.UUID4 | None,
    faculty_id: pydantic.UUID4 | None,
    department_id: pydantic.UUID4 | None,
) -> ConnectionModel | None:
    query = select(ConnectionModel)

    if group_id:
        query = query.filter(ConnectionModel.group_id == group_id)
    if faculty_id:
        query = query.filter(ConnectionModel.faculty_id == faculty_id)
    if department_id:
        query = query.filter(ConnectionModel.department_id == department_id)

    return session.exec(query).first()
