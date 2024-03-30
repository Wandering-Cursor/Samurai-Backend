import uuid
from typing import TYPE_CHECKING

import pydantic
from sqlmodel import Field, Relationship

from samurai_backend.models.projects.task import BaseTask, TaskRepresentation

if TYPE_CHECKING:
    from samurai_backend.models.user_projects.project import UserProjectModel


class UserTaskRepresentation(TaskRepresentation):
    pass


class UserTaskModel(BaseTask, table=True):
    task_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )

    project_id: pydantic.UUID4 = Field(foreign_key="userprojectmodel.project_id")
    project: "UserProjectModel" = Relationship(back_populates="tasks")
