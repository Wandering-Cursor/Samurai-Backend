from collections import defaultdict
from typing import Annotated

import pydantic

from samurai_backend.account.schemas.account_by_account_id_mixin import AccountByAccountIdMixin
from samurai_backend.core.schemas import BasePaginatedResponse, PaginationSearchSchema
from samurai_backend.enums import TaskState
from samurai_backend.models.projects.project import (
    ProjectRepresentation,
    ShortProjectRepresentation,
)
from samurai_backend.models.user_projects.task import UserTaskRepresentation
from samurai_backend.user_projects.schemas.user_project_link import UserProjectLinkRepresentation


class ProjectSearchInput(PaginationSearchSchema):
    account_id: pydantic.UUID4 | None = pydantic.Field(
        default=None,
        description="If not specified, searches for projects related to the current account",
    )
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


class ProjectStatsEntity(pydantic.BaseModel):
    total: int


class ProjectStatsByTeacher(AccountByAccountIdMixin):
    projects: ProjectStatsEntity
    tasks: dict[TaskState, int]
    tasks_total: int


ProjectsStatsByTeacher = Annotated[
    list[ProjectStatsByTeacher],
    pydantic.Field(default_factory=list),
]
