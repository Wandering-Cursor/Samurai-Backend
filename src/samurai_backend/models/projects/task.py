import datetime
import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship

from .base import BaseNamed

if TYPE_CHECKING:
    from .project import ProjectModel


class BaseTask(BaseNamed):
    priority: int = Field(
        default=0,
        description="Priority of the task. Higher number means that this task is more important.",
    )

    name: str = Field(
        description="Name of the task.",
    )
    reviewer: uuid.UUID | None = Field(
        default=None,
        nullable=True,
        foreign_key="accountmodel.account_id",
        description="Account ID of the reviewer of the task.",
    )
    due_date: datetime.datetime | None = Field(
        default=None,
        description="Due date of the task (optional).",
    )

    project_id: pydantic.UUID4 = Field(
        foreign_key="projectmodel.project_id",
        index=True,
        description="Project ID of the project this task belongs to.",
    )


class CreateTask(BaseTask):
    pass


class TaskRepresentation(BaseTask):
    task_id: pydantic.UUID4


class TaskRepresentationShortDescription(TaskRepresentation):
    @pydantic.field_validator("description", mode="before")
    @classmethod
    def convert_description(cls, value: str | None) -> str | None:
        max_length = 128

        if value is None:
            return None
        return value[:max_length] + "..." if len(value) > max_length else value


class TaskModel(BaseTask, table=True):
    task_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )

    project: "ProjectModel" = Relationship(back_populates="tasks")
