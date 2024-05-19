from typing import TypeVar

import pydantic
from sqlmodel import Session

from samurai_backend.account.schemas.account.account import AccountCreateConnectionForBatch
from samurai_backend.admin.get.connections import get_connection, get_connection_by_parameters
from samurai_backend.core.operations import store_entity
from samurai_backend.models.account.connection import ConnectionModel

T = TypeVar("T")


def add_connections(session: Session, entity: T, connections: list[pydantic.UUID4]) -> T:
    entity.connections = [
        get_connection(
            session=session,
            connection_id=connection_id,
        )
        for connection_id in connections
    ]
    return entity


def get_or_create_connection(
    session: Session,
    connection_parameters: AccountCreateConnectionForBatch,
    commit: bool = True,
) -> ConnectionModel:
    connection = get_connection_by_parameters(
        session=session,
        group_id=connection_parameters.group_id,
        faculty_id=connection_parameters.faculty_id,
        department_id=connection_parameters.department_id,
    )

    if not connection:
        connection = ConnectionModel(
            group_id=connection_parameters.group_id,
            faculty_id=connection_parameters.faculty_id,
            department_id=connection_parameters.department_id,
        )

        connection = store_entity(session, connection)
        if commit:
            session.commit()

    return connection


def add_connections_for_batch(
    session: Session,
    entity: T,
    connections: list[AccountCreateConnectionForBatch],
    commit: bool = True,
) -> T:
    entity.connections = [
        get_or_create_connection(
            session=session,
            connection_parameters=connection,
            commit=False,
        )
        for connection in connections
    ]

    if commit:
        session.commit()

    return entity
