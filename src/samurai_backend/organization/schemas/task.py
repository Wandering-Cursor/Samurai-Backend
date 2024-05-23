import pydantic

from samurai_backend.models.projects.task import TaskRepresentation
from samurai_backend.schemas import BasePaginatedResponse, PaginationSearchSchema


class TaskSearchInput(PaginationSearchSchema):
    project_id: pydantic.UUID4 | None = None
    name: str | None = None


class TaskSearchOutput(BasePaginatedResponse):
    content: list[TaskRepresentation]
