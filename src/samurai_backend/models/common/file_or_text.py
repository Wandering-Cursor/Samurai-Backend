import uuid
from typing import TYPE_CHECKING

import sqlmodel

from samurai_backend.models.base import BaseModel

if TYPE_CHECKING:
    from samurai_backend.models.communication.message import MessageModel
    from samurai_backend.models.user_projects.comment import CommentModel


class FileModel(BaseModel, table=True):
    file_id: uuid.UUID = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )

    file_name: str = sqlmodel.Field(
        max_length=255,
    )
    file_type: str = sqlmodel.Field(
        max_length=255,
    )
    file_size: int = sqlmodel.Field(
        ge=0,
    )

    file_path: str = sqlmodel.Field(
        exclude=True,
    )

    uploaded_by_id: uuid.UUID = sqlmodel.Field(
        foreign_key="accountmodel.account_id",
    )

    comment: "CommentModel" = sqlmodel.Relationship(back_populates="file")
    message: "MessageModel" = sqlmodel.Relationship(back_populates="file")


class FileOrTextMixin(BaseModel):
    file_id: uuid.UUID | None = sqlmodel.Field(
        default=None,
        foreign_key="filemodel.file_id",
        nullable=True,
    )
    text: str | None = sqlmodel.Field(
        default=None,
        nullable=True,
    )
