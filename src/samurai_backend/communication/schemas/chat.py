import pydantic

from samurai_backend.account.schemas.account.account_representation import (
    AccountRepresentation,
)
from samurai_backend.core.schemas import BasePaginatedResponse, PaginationSearchSchema


class ChatUpdate(pydantic.BaseModel):
    name: str | None = pydantic.Field(
        default=None,
        examples=[None, "My chat"],
    )


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
            "self": f"/communication/chat/{self.chat_id}",
            "messages": f"/communication/messages/{self.chat_id}",
            "participants": f"/communication/chat/{self.chat_id}/participants",
        }


class ChatsSearchSchema(PaginationSearchSchema):
    name: str | None = pydantic.Field(
        default=None,
    )


class ChatsSearchResponse(BasePaginatedResponse):
    content: list[ChatRepresentation]


class ChatAddMember(pydantic.BaseModel):
    account_ids: list[pydantic.UUID4]


class ChatLeaveResponse(pydantic.BaseModel):
    left: bool = pydantic.Field(
        exclude=True,
    )

    @pydantic.computed_field
    def message(self: "ChatLeaveResponse") -> str:
        if self.left:
            return "You have left the chat."
        return "You are not a member of this chat."


class ChatParticipantsSearchSchema(PaginationSearchSchema):
    pass


class ChatParticipantsResponse(BasePaginatedResponse):
    content: list[AccountRepresentation]

    @staticmethod
    def to_representation(
        participants: list,
    ) -> list[AccountRepresentation]:
        return [
            AccountRepresentation.model_validate(
                participant,
                from_attributes=True,
            )
            for participant in participants
        ]
