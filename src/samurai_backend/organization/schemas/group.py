import pydantic

from samurai_backend.models.organization.group import Group
from samurai_backend.schemas import BasePaginatedResponse, PaginationSearchSchema


class GroupSearchInput(PaginationSearchSchema):
    faculty_id: pydantic.UUID4 | None = None
    name: str | None = None


class GroupSearchOutput(BasePaginatedResponse):
    content: list[Group]
