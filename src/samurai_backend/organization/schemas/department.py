import pydantic

from samurai_backend.core.schemas import BasePaginatedResponse, PaginationSearchSchema
from samurai_backend.models.organization.department import DepartmentRepresentation


class DepartmentSearchInput(PaginationSearchSchema):
    name: str | None = pydantic.Field(
        default=None, description="Name of the department, full, or partial match."
    )


class DepartmentSearchOutput(BasePaginatedResponse):
    content: list[DepartmentRepresentation]
