from typing import Literal

import pydantic


class WSKeys:
    @staticmethod
    def chats_key(account_id: int) -> str:
        return f"chats:{account_id}"


chat_event = Literal["created", "updated", "member_added", "member_left"]


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
