import datetime
import uuid

import pydantic

from samurai_backend.account.schemas.account_by_account_id_mixin import AccountByAccountIdMixin
from samurai_backend.schemas import BasePaginatedResponse, PaginationSearchSchema


class MessageUpdate(pydantic.BaseModel):
    text: str | None = pydantic.Field(
        default=None,
        examples=[None, "Hello, world!"],
    )
    file_id: pydantic.UUID4 | None = pydantic.Field(
        default=None,
        examples=[None, str(uuid.uuid4())],
    )

    @pydantic.model_validator(mode="after")
    def validate_update(self: "MessageUpdate") -> "MessageUpdate":
        if self.text is None and self.file_id is None:
            raise ValueError("At least one of `text` or `file_id` must be provided.")
        return self


class MessageCreate(pydantic.BaseModel):
    chat_id: pydantic.UUID4
    text: str | None = pydantic.Field(
        default=None,
        examples=[None, "Hello, world!"],
    )
    file_id: pydantic.UUID4 | None = pydantic.Field(
        default=None,
        examples=[None, str(uuid.uuid4())],
    )


class MessageRepresentation(pydantic.BaseModel):
    chat_id: pydantic.UUID4
    message_id: pydantic.UUID4
    sender_id: pydantic.UUID4

    text: str | None = pydantic.Field(
        default=None,
        examples=[None, "Hello, world!"],
    )
    file_id: pydantic.UUID4 | None = pydantic.Field(
        default=None,
        examples=[None, str(uuid.uuid4())],
    )
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @pydantic.computed_field
    def _links(self: "MessageRepresentation") -> dict[str, str]:
        return {
            "self": f"/communication/message/{self.message_id}",
            "chat": f"/communication/chat/{self.chat_id}",
            "sender": f"/account/{self.sender_id}/info",
            "seen_by": f"/communication/message/{self.message_id}/seen_by",
            "file": f"/common/file/{self.file_id}" if self.file_id else None,
        }


class MessagesSearchSchema(PaginationSearchSchema):
    chat_id: pydantic.UUID4

    text: str | None = pydantic.Field(
        default=None,
    )
    file_only: bool = pydantic.Field(
        default=False,
    )

    sent_after: datetime.datetime | None = pydantic.Field(
        default=None,
        description="Can be used for offset pagination, since UUIDs are not sequential.",
    )
    sent_before: datetime.datetime | None = pydantic.Field(
        default=None,
    )
    descending: bool = pydantic.Field(
        default=True,
        description=(
            "`true` - scrolling up, `false` - scrolling down. "
            "Set to `false` when you are jumping to a specific message."
            "(Using `sent_after` as offset)"
        ),
    )


class MessagesSearchResponse(BasePaginatedResponse):
    content: list[MessageRepresentation]


class MessageSeenByRepresentation(AccountByAccountIdMixin):
    message_id: pydantic.UUID4
    at_time: datetime.datetime


class MessageSeenByResponse(pydantic.BaseModel):
    seen_by: list[MessageSeenByRepresentation]

    @staticmethod
    def from_seen_by(viewers: list) -> "MessageSeenByResponse":
        seen_by = []

        for viewer in viewers:
            seen_by.append(
                MessageSeenByRepresentation(
                    account_id=viewer.account_id,
                    message_id=viewer.message_id,
                    at_time=viewer.at_time,
                )
            )

        return MessageSeenByResponse(
            seen_by=seen_by,
        )
