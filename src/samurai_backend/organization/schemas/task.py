import pydantic

from samurai_backend.core.schemas import BasePaginatedResponse, PaginationSearchSchema
from samurai_backend.models.projects.task import TaskRepresentation


class TaskSearchInput(PaginationSearchSchema):
    project_id: pydantic.UUID4 | None = None
    name: str | None = None


class TaskSearchOutput(BasePaginatedResponse):
    content: list[TaskRepresentation]
