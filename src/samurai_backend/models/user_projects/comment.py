from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import pydantic
from sqlmodel import Field, Relationship

from samurai_backend.models.common.file_or_text import FileModel, FileOrTextMixin

if TYPE_CHECKING:
    from samurai_backend.models.user_projects.task import UserTaskModel


class CreateComment(FileOrTextMixin):
    task_id: pydantic.UUID4
    sender_id: pydantic.UUID4


class CommentModel(FileOrTextMixin, table=True):
    comment_id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        unique=True,
    )

    task_id: UUID = Field(
        foreign_key="usertaskmodel.task_id",
        index=True,
    )
    sender_id: UUID = Field(
        foreign_key="accountmodel.account_id",
        index=True,
    )

    file: FileModel = Relationship(back_populates="comment")
    task: "UserTaskModel" = Relationship(back_populates="comments")
