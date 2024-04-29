import pydantic

from samurai_backend.core.schemas import BasePaginatedResponse, PaginationSearchSchema
from samurai_backend.models.account.connection import ConnectionBase


class ConnectionRepresentation(ConnectionBase):
    pass


class ConnectionsFilter(PaginationSearchSchema):
    connection_id: pydantic.UUID4 | None = None

    group_id: pydantic.UUID4 | None = None
    faculty_id: pydantic.UUID4 | None = None
    department_id: pydantic.UUID4 | None = None


class ConnectionsPaginatedResponse(BasePaginatedResponse):
    content: list[ConnectionRepresentation]
