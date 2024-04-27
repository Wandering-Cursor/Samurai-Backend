import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from samurai_backend.models.base import BaseModel
from samurai_backend.models.communication.chat_account_link import ChatAccountLinkModel
from samurai_backend.utils.random_names import get_random_name

if TYPE_CHECKING:
    from sqlmodel import Session

    from samurai_backend.models.account.account import AccountModel


class ChatModel(BaseModel, table=True):
    chat_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )

    name: str = Field(default_factory=get_random_name)

    participant_links: list[ChatAccountLinkModel] = Relationship(
        back_populates="chat",
    )

    def create_link(
        self: "ChatModel", session: "Session", account: "AccountModel"
    ) -> ChatAccountLinkModel | None:
        if self.is_member(account):
            return None

        link = ChatAccountLinkModel(
            chat_id=self.chat_id,
            account_id=account.account_id,
        )
        session.add(link)
        self.participant_links.append(link)
        return link

    def is_member(self: "ChatModel", account: "AccountModel") -> bool:
        return any(link.account_id == account.account_id for link in self.participant_links)
