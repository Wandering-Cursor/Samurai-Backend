from collections import defaultdict

import pydantic

from samurai_backend.core.schemas import BasePaginatedResponse, PaginationSearchSchema
from samurai_backend.enums import TaskState
from samurai_backend.models.projects.project import (
    ProjectRepresentation,
    ShortProjectRepresentation,
)
from samurai_backend.models.user_projects.task import UserTaskRepresentation
from samurai_backend.models.user_projects.user_project_link import UserProjectLinkRepresentation


class ProjectSearchInput(PaginationSearchSchema):
    faculty_id: pydantic.UUID4 | None = None
    name: str | None = None


class ShortUserProjectRepresentation(ShortProjectRepresentation):
    account_links: list[UserProjectLinkRepresentation]

    @pydantic.computed_field
    @property
    def _links(self) -> dict[str, dict[str, str]]:
        return {
            "self": {"href": f"/projects/project/{self.project_id}"},
            "tasks": {"href": f"/projects/tasks/{self.project_id}"},
        }

    @pydantic.field_validator("account_links", mode="before")
    @classmethod
    def convert_account_links(
        cls, value: list[UserProjectLinkRepresentation | object]
    ) -> list[UserProjectLinkRepresentation]:
        values = []
        for item in value:
            if isinstance(item, UserProjectLinkRepresentation):
                values.append(item)
            elif isinstance(item, pydantic.BaseModel):
                values.append(UserProjectLinkRepresentation(**item.model_dump()))
            elif isinstance(item, dict):
                values.append(UserProjectLinkRepresentation(**item))
            else:
                raise ValueError("Invalid type")
        return values


class UserProjectRepresentation(ProjectRepresentation):
    tasks: list[UserTaskRepresentation]
    account_links: list[UserProjectLinkRepresentation]

    @pydantic.computed_field
    @property
    def tasks_count_by_status(self: "UserProjectRepresentation") -> dict[TaskState, int]:
        result = defaultdict(int)
        for state in TaskState:
            result[state.value] = 0

        for task in self.tasks:
            result[task.state] += 1

        return result


class UserProjectSearchOutput(BasePaginatedResponse):
    content: list[ShortUserProjectRepresentation]
