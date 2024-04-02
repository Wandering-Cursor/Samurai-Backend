import pydantic

from samurai_backend.core.schemas import BasePaginatedResponse, PaginationSearchSchema
from samurai_backend.enums import TaskState
from samurai_backend.models.user_projects.task import UserTaskRepresentation


class UserTaskSearchInput(PaginationSearchSchema):
    name: str | None = None


class UserTaskSearch(UserTaskSearchInput):
    account_id: pydantic.UUID4
    project_id: pydantic.UUID4


class UserTaskSearchOutput(BasePaginatedResponse):
    content: list[UserTaskRepresentation]


class UserTaskStatusUpdateInput(pydantic.BaseModel):
    state: TaskState
