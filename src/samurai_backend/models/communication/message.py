import datetime
import uuid

from sqlmodel import Field, Relationship, SQLModel

from samurai_backend.models.common.file_or_text import FileOrTextMixin
from samurai_backend.utils.current_time import current_time


class MessageSeenBy(SQLModel, table=True):
    account_id: uuid.UUID = Field(
        foreign_key="accountmodel.account_id",
        primary_key=True,
    )
    message_id: uuid.UUID = Field(
        foreign_key="messagemodel.message_id",
        primary_key=True,
    )
    at_time: datetime.datetime = Field(
        default_factory=current_time,
    )

    message: "MessageModel" = Relationship(back_populates="seen_by")


class MessageModel(FileOrTextMixin, table=True):
    message_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )

    sender_id: uuid.UUID = Field(
        foreign_key="accountmodel.account_id",
    )
    chat_id: uuid.UUID = Field(
        foreign_key="chatmodel.chat_id",
    )

    seen_by: list[MessageSeenBy] = Relationship(
        back_populates="message",
    )

    def add_seen_by(self, account_id: uuid.UUID) -> None:
        """Add a user to the list of users who have seen the message."""
        self.seen_by.append(
            MessageSeenBy(
                account_id=account_id,
                message_id=self.message_id,
            ),
        )
