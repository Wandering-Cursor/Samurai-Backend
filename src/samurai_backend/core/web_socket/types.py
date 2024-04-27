from typing import Literal

import pydantic

from samurai_backend.account.schemas.account_by_account_id_mixin import AccountByAccountIdMixin
from samurai_backend.communication.schemas.message import (
    MessageRepresentation,
    MessageSeenByRepresentation,
)


class WSKeys:
    @staticmethod
    def chats_key(account_id: pydantic.UUID4) -> str:
        return f"chats:{account_id}"

    @staticmethod
    def messages_key(chat_id: pydantic.UUID4) -> str:
        return f"messages:{chat_id}"


chat_event = Literal["created", "updated", "member_added", "member_left"]
message_events = Literal["created", "updated", "typing", "read"]


class WebSocketCommand(pydantic.BaseModel):
    action: str
    data: dict | None = None


class ConnectedResponse(pydantic.BaseModel):
    message: str = "connected"
    commands: list[str]


class WSError(pydantic.BaseModel):
    error: str = "Invalid data"
    message: dict | str | None = None


class ChatEvent(pydantic.BaseModel):
    chat_entity: object = pydantic.Field(exclude=True)

    event_type: chat_event
    additional_context: dict | None = None

    @pydantic.computed_field
    def chat(self: "ChatEvent") -> dict:
        from samurai_backend.communication.schemas.chat import ChatRepresentation

        return ChatRepresentation.model_validate(
            self.chat_entity,
            from_attributes=True,
        ).model_dump(mode="json")


class TyperData(AccountByAccountIdMixin):
    chat_id: pydantic.UUID4


class MessageEvent(pydantic.BaseModel):
    entity: MessageRepresentation | None = pydantic.Field(None)
    seen_by: MessageSeenByRepresentation | None = pydantic.Field(None)
    typer: TyperData | None = pydantic.Field(None)

    event_type: message_events

    @pydantic.field_validator("seen_by", mode="before")
    @classmethod
    def validate_seen_by(cls, value: dict | None) -> MessageSeenByRepresentation | None:
        if value is None:
            return None

        return MessageSeenByRepresentation.model_validate(value, from_attributes=True)

    @pydantic.field_validator("entity", mode="before")
    @classmethod
    def validate_entity(cls, value: dict | None) -> MessageRepresentation | None:
        if value is None:
            return None

        return MessageRepresentation.model_validate(value, from_attributes=True)
