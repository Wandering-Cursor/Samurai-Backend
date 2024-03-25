import pydantic

from samurai_backend.core.schemas import BasePaginatedResponse, PaginationSearchSchema
from samurai_backend.models.organization.faculty import FacultyRepresentation


class FacultySearchInput(PaginationSearchSchema):
    department_id: pydantic.UUID4 | None = None
    name: str | None = None


class FacultySearchOutput(BasePaginatedResponse):
    content: list[FacultyRepresentation]
