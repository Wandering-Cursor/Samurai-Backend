import uuid

import pydantic
from sqlmodel import Field, Relationship

from .base import BaseNamed
from .task import TaskModel


class BaseProject(BaseNamed):
    faculty_id: pydantic.UUID4 = Field(
        foreign_key="facultymodel.faculty_id",
    )


class CreateProject(BaseProject):
    pass


class ShortProjectRepresentation(BaseProject):
    project_id: pydantic.UUID4
    tasks: list = pydantic.Field(default_factory=list, exclude=True)

    @pydantic.computed_field
    @property
    def tasks_count(self) -> int:
        return len(self.tasks)

    @pydantic.computed_field
    @property
    def _links(self) -> dict[str, dict[str, str]]:
        return {
            "self": {"href": f"/admin/project/{self.project_id}"},
            "tasks": {"href": f"/admin/tasks?project_id={self.project_id}"},
        }


class ProjectRepresentation(ShortProjectRepresentation):
    project_id: pydantic.UUID4
    tasks: list[TaskModel] = pydantic.Field(description="Tasks of the project (up to 5)")

    @pydantic.field_validator("tasks", mode="before")
    @classmethod
    def convert_tasks(cls, value: list[TaskModel | dict]) -> list[TaskModel]:
        return value[:5]


class ProjectModel(BaseProject, table=True):
    project_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )

    tasks: list[TaskModel] = Relationship(back_populates="project")
