import pydantic

from samurai_backend.core.schemas import BasePaginatedResponse, PaginationSearchSchema
from samurai_backend.models.projects.project import ProjectRepresentation


class ProjectSearchInput(PaginationSearchSchema):
    faculty_id: pydantic.UUID4 | None = None
    name: str | None = None


class ProjectSearchOutput(BasePaginatedResponse):
    content: list[ProjectRepresentation]
