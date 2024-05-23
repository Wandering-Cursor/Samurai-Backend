import uuid

import pydantic
import sqlalchemy as sa
from sqlmodel import Field, Relationship

from samurai_backend.enums.task_state import TaskState
from samurai_backend.models.projects.task import BaseTask, CreateTask, TaskRepresentation
from samurai_backend.models.user_projects.comment import CommentModel
from samurai_backend.models.user_projects.project import UserProjectModel


class UserTaskCreate(CreateTask):
    state: TaskState
    project_id: pydantic.UUID4


class UserTaskRepresentation(TaskRepresentation):
    state: TaskState
    comments: list = pydantic.Field(default_factory=list, exclude=True)

    @pydantic.computed_field
    @property
    def comment_count(self) -> int:
        return len(self.comments)


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

    project_id: pydantic.UUID4 = Field(
        sa_column=sa.Column(
            sa.UUID(),
            sa.ForeignKey("userprojectmodel.project_id", ondelete="CASCADE"),
            index=True,
        ),
    )
    project: UserProjectModel = Relationship(back_populates="tasks")
    comments: list[CommentModel] = Relationship(
        back_populates="task",
    )
