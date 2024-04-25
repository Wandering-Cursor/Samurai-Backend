from typing import TYPE_CHECKING

from samurai_backend.account.get.account import get_account_by_id
from samurai_backend.communication.get.chat import get_chat
from samurai_backend.communication.operations.message import remove_all_messages_by_chat_id
from samurai_backend.communication.schemas import chat as chat_schemas
from samurai_backend.core.operations import delete_entity
from samurai_backend.dependencies import account_type, database_session_type
from samurai_backend.log import events_logger
from samurai_backend.models.communication.chat import ChatModel

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from pydantic.types import UUID4


async def create_chat(
    session: database_session_type,
    create_chat: chat_schemas.ChatCreate,
    current_user: account_type,
) -> ChatModel:
    entity = ChatModel(
        name=create_chat.name,
    )
    session.add(entity)
    session.commit()

    participants = [current_user.account_id] + (create_chat.participants or [])
    for account_id in participants:
        account = get_account_by_id(session=session, account_id=account_id)
        entity.create_link(account=account, session=session)

    session.commit()

    return entity


async def update_chat(
    session: database_session_type,
    chat: ChatModel,
    chat_update: chat_schemas.ChatUpdate,
) -> ChatModel:
    chat.name = chat_update.name or chat.name
    chat.update_time()

    session.add(chat)
    session.commit()

    return chat


async def add_chat_member(
    session: database_session_type,
    chat: ChatModel,
    add_member_input: chat_schemas.ChatAddMember,
) -> ChatModel:
    for account_id in add_member_input.account_ids:
        account = get_account_by_id(session=session, account_id=account_id)
        if not account:
            continue

        chat.create_link(session=session, account=account)

    session.commit()

    return chat


async def leave_chat(
    session: database_session_type,
    chat: ChatModel,
    account: account_type,
) -> bool:
    link = next(
        (link for link in chat.participant_links if link.account_id == account.account_id),
        None,
    )
    if not link:
        return False

    chat.participant_links.remove(link)
    delete_entity(session=session, entity=link)

    session.add(chat)
    session.commit()

    return True


async def remove_empty_chat(
    session: "AsyncGenerator[database_session_type, None]",
    chat_id: "UUID4",
) -> None:
    session: database_session_type = await session.__anext__()

    chat = await get_chat(session=session, chat_id=chat_id)
    if not chat:
        return
    if len(chat.participant_links) > 0:
        return

    events_logger.info(f"Removing empty chat: {chat.chat_id}")

    await remove_all_messages_by_chat_id(session=session, chat_id=chat.chat_id, commit=False)
    delete_entity(session=session, entity=chat, commit=False)

    session.commit()

    events_logger.info(f"Chat removed: {chat.chat_id}")
