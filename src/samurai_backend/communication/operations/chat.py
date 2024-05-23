from typing import TYPE_CHECKING

from sqlmodel import Session

from samurai_backend.account.get.account import get_account_by_id
from samurai_backend.account.schemas.account_by_account_id_mixin import AccountByAccountIdMixin
from samurai_backend.communication.get.chat import get_chat
from samurai_backend.communication.operations.message import remove_all_messages_by_chat_id
from samurai_backend.communication.schemas import chat as chat_schemas
from samurai_backend.core.operations import delete_entity
from samurai_backend.core.web_socket.manager import web_socket_manager
from samurai_backend.core.web_socket.types import ChatEvent, WSKeys
from samurai_backend.log import events_logger
from samurai_backend.models.account.account import AccountModel
from samurai_backend.models.communication.chat import ChatModel

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from pydantic.types import UUID4


async def chat_updated_event(
    chat: ChatModel,
    event: ChatEvent,
    additional_context: dict | None = None,
) -> None:
    for link in chat.participant_links:
        await web_socket_manager.broadcast(
            WSKeys.chats_key(link.account_id),
            ChatEvent(
                chat_id=chat.chat_id,
                chat_entity=chat,
                event_type=event,
                additional_context=additional_context,
            ).model_dump(),
        )


async def create_chat(
    session: Session,
    body: chat_schemas.ChatCreate,
    current_user: AccountModel,
) -> ChatModel:
    entity = ChatModel(
        name=body.name,
    )
    session.add(entity)
    session.commit()

    participants = [current_user.account_id] + (body.participants or [])
    for account_id in participants:
        account = get_account_by_id(session=session, account_id=account_id)
        entity.create_link(account=account, session=session)

    session.commit()

    await chat_updated_event(chat=entity, event="created")

    return entity


async def update_chat(
    session: Session,
    chat: ChatModel,
    chat_update: chat_schemas.ChatUpdate,
) -> ChatModel:
    chat.name = chat_update.name or chat.name
    chat.update_time()

    session.add(chat)
    session.commit()

    await chat_updated_event(chat=chat, event="updated")

    return chat


async def add_chat_member(
    session: Session,
    chat: ChatModel,
    add_member_input: chat_schemas.ChatAddMember,
) -> ChatModel:
    new_members = []

    for account_id in add_member_input.account_ids:
        account = get_account_by_id(session=session, account_id=account_id)
        if not account:
            continue

        link = chat.create_link(session=session, account=account)
        if link:
            new_members.append(account)

    session.commit()

    await chat_updated_event(
        chat=chat,
        event="member_added",
        additional_context={
            "new_members": [
                AccountByAccountIdMixin(
                    account_id=account.account_id,
                ).model_dump(mode="json")
                for account in new_members
            ],
        },
    )

    return chat


async def leave_chat(
    session: Session,
    chat: ChatModel,
    account: AccountModel,
) -> bool:
    link = next(
        (link for link in chat.participant_links if link.account_id == account.account_id),
        None,
    )
    if not link:
        return False

    await chat_updated_event(
        chat=chat,
        event="member_left",
        additional_context={
            "member": AccountByAccountIdMixin(
                account_id=account.account_id,
            ).model_dump(mode="json"),
        },
    )

    chat.participant_links.remove(link)
    delete_entity(session=session, entity=link)

    session.add(chat)
    session.commit()
    return True


async def remove_empty_chat(
    session: "AsyncGenerator[Session, None]",
    chat_id: "UUID4",
) -> None:
    session: Session = await anext(session)

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
