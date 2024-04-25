from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import select

from samurai_backend.communication.schemas.chat import ChatRepresentation, ChatsSearchResponse
from samurai_backend.errors import SamuraiNotFoundError
from samurai_backend.models.communication.chat import ChatModel
from samurai_backend.models.communication.chat_account_link import ChatAccountLinkModel
from samurai_backend.utils.get_count import get_count

if TYPE_CHECKING:
    from pydantic.types import UUID4
    from sqlmodel import Session

    from samurai_backend.communication.schemas.chat import ChatsSearchSchema
    from samurai_backend.dependencies import account_type


async def get_chat(
    session: Session,
    chat_id: UUID4,
) -> ChatModel:
    search = select(ChatModel).filter(
        ChatModel.chat_id == chat_id,
    )

    chat = session.exec(search).first()

    if not chat:
        raise SamuraiNotFoundError

    return chat


async def get_related_chat(
    session: Session,
    chat_id: UUID4,
    current_user: account_type,
) -> ChatModel:
    chat = await get_chat(
        session=session,
        chat_id=chat_id,
    )

    if not chat.is_member(current_user):
        raise SamuraiNotFoundError

    return chat


async def get_user_chats(
    session: Session,
    current_user: account_type,
    search_params: ChatsSearchSchema,
) -> ChatsSearchResponse:
    search = select(ChatModel).filter(
        ChatModel.participant_links.any(
            ChatAccountLinkModel.account_id == current_user.account_id,
        )
    )

    if search_params.name:
        search = search.filter(ChatModel.name.icontains(search_params.name))

    total = get_count(session, search)
    query = search.offset(search_params.offset).limit(search_params.page_size)

    chats = session.exec(query)

    return ChatsSearchResponse(
        content=[ChatRepresentation.model_validate(chat, from_attributes=True) for chat in chats],
        meta=ChatsSearchResponse.construct_meta(
            total=total,
            page=search_params.page,
            page_size=search_params.page_size,
        ),
    )
