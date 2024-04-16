import pydantic


class ChatCreate(pydantic.BaseModel):
    name: str | None = pydantic.Field(
        default=None,
        examples=[None, "My chat"],
    )
    participants: list[pydantic.UUID4] | None = pydantic.Field(
        default=None,
        examples=[None, []],
    )


class ChatRepresentation(pydantic.BaseModel):
    chat_id: pydantic.UUID4
    name: str

    @pydantic.computed_field
    def _links(self: "ChatRepresentation") -> dict[str, str]:
        return {
            "self": f"/chat/{self.chat_id}",
            "messages": f"/chat/{self.chat_id}/messages",
            "participants": f"/chat/{self.chat_id}/participants",
        }
