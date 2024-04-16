import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from samurai_backend.models.account.account import AccountModel
    from samurai_backend.models.communication.chat import ChatModel


class ChatAccountLinkModel(SQLModel, table=True):
    account_id: uuid.UUID = Field(
        foreign_key="accountmodel.account_id",
        primary_key=True,
    )
    chat_id: uuid.UUID = Field(
        foreign_key="chatmodel.chat_id",
        primary_key=True,
    )

    chat: "ChatModel" = Relationship(back_populates="participant_links")
    account: "AccountModel" = Relationship(back_populates="chat_links")
