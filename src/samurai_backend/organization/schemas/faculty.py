import pydantic

from samurai_backend.models.organization.faculty import FacultyRepresentation
from samurai_backend.schemas import BasePaginatedResponse, PaginationSearchSchema


class FacultySearchInput(PaginationSearchSchema):
    department_id: pydantic.UUID4 | None = None
    name: str | None = None


class FacultySearchOutput(BasePaginatedResponse):
    content: list[FacultyRepresentation]
