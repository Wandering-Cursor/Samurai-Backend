import datetime
import uuid

import pydantic


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
            "self": f"/message/{self.message_id}",
            "chat": f"/chat/{self.chat_id}",
            "sender": f"/account/{self.sender_id}",
        }
