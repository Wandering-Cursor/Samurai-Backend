import pydantic

from samurai_backend.models.organization.department import DepartmentRepresentation
from samurai_backend.schemas import BasePaginatedResponse, PaginationSearchSchema


class DepartmentSearchInput(PaginationSearchSchema):
    name: str | None = pydantic.Field(
        default=None, description="Name of the department, full, or partial match."
    )


class DepartmentSearchOutput(BasePaginatedResponse):
    content: list[DepartmentRepresentation]
