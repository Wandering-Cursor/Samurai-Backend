import uuid

import pydantic
from sqlmodel import Field, Relationship

from .base import BaseNamed
from .task import TaskModel, TaskRepresentationShortDescription


class BaseProject(BaseNamed):
    faculty_id: pydantic.UUID4 = Field(
        foreign_key="facultymodel.faculty_id",
    )


class CreateProject(BaseProject):
    pass


class ShortProjectRepresentation(BaseProject):
    project_id: pydantic.UUID4
    tasks: list[TaskRepresentationShortDescription] = pydantic.Field(
        default_factory=list, exclude=True
    )

    @pydantic.field_validator("description", mode="before")
    @classmethod
    def convert_description(cls, value: str | None) -> str | None:
        max_length = 128

        if value is None:
            return None
        return value[:max_length] + "..." if len(value) > max_length else value

    @pydantic.computed_field
    @property
    def tasks_total(self) -> int:
        return len(self.tasks)

    @pydantic.computed_field
    @property
    def _links(self) -> dict[str, dict[str, str]]:
        return {
            "self": {"href": f"/admin/project/{self.project_id}"},
            "tasks": {"href": f"/admin/tasks?project_id={self.project_id}"},
        }


class ProjectRepresentationFull(BaseProject):
    project_id: pydantic.UUID4
    tasks: list[TaskRepresentationShortDescription] = pydantic.Field(
        description="Tasks of the project"
    )


class ProjectRepresentation(ProjectRepresentationFull):
    @pydantic.field_validator(
        "tasks", mode="after"
    )  # If this doesn't work, add a property to get all tasks
    @classmethod
    def convert_tasks(
        cls, value: list[TaskRepresentationShortDescription | dict]
    ) -> list[TaskRepresentationShortDescription]:
        return value[:5]


class ProjectModel(BaseProject, table=True):
    project_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )

    tasks: list[TaskModel] = Relationship(back_populates="project")
