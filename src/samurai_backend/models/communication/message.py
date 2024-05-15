import datetime
import html
import uuid

from sqlmodel import Field, Relationship, SQLModel

from samurai_backend.errors import SamuraiValidationError
from samurai_backend.models.common.file_or_text import FileModel, FileOrTextMixin
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

    file: FileModel = Relationship(back_populates="message")

    def add_seen_by(self, account_id: uuid.UUID) -> MessageSeenBy:
        """Add a user to the list of users who have seen the message."""
        seen_by = MessageSeenBy(
            account_id=account_id,
            message_id=self.message_id,
        )

        self.seen_by.append(seen_by)

        return seen_by

    def is_seen(
        self: "MessageModel",
        account_id: uuid.UUID,
    ) -> bool:
        """Check if the message is seen by the user."""
        return any(seen_by.account_id == account_id for seen_by in self.seen_by)

    def set_text(self: "MessageModel", text: str | None) -> None:
        """Set the text of the message."""
        if text is None:
            return

        escaped_text = html.escape(text)
        if len(escaped_text.strip()) == 0:
            raise SamuraiValidationError(message="Message text cannot be empty.")

        self.text = escaped_text
