import uuid

import pydantic
from sqlmodel import Field, Relationship

from samurai_backend.enums import TaskState
from samurai_backend.models.projects.task import BaseTask, TaskRepresentation
from samurai_backend.models.user_projects.project import UserProjectModel


class UserTaskRepresentation(TaskRepresentation):
    state: TaskState


class UserTaskModel(BaseTask, table=True):
    task_id: pydantic.UUID4 = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
    )
    state: TaskState = Field(
        default=TaskState.OPEN,
        index=True,
    )

    project_id: pydantic.UUID4 = Field(foreign_key="userprojectmodel.project_id", index=True)
    project: UserProjectModel = Relationship(back_populates="tasks")
