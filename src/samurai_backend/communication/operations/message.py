from pydantic.types import UUID4
from sqlmodel import Session, delete

from samurai_backend.communication.schemas import message as message_schema
from samurai_backend.core.web_socket.manager import web_socket_manager
from samurai_backend.core.web_socket.types import MessageEvent, TyperData, WSKeys
from samurai_backend.errors import (
    SamuraiForbiddenError,
    SamuraiNotFoundError,
)
from samurai_backend.log import events_logger
from samurai_backend.models.account.account import AccountModel
from samurai_backend.models.communication.message import MessageModel, MessageSeenBy


async def create_message(
    session: Session,
    body: message_schema.MessageCreate,
    current_user: AccountModel,
) -> MessageModel:
    """Create a message."""
    message_entity = MessageModel(
        chat_id=body.chat_id,
        sender_id=current_user.account_id,
        file_id=body.file_id,
    )
    message_entity.set_text(body.text)

    message_entity.add_seen_by(current_user.account_id)

    session.add(message_entity)
    session.commit()

    await send_new_message_ws_event(message_entity)

    return message_entity


async def remove_all_messages_by_chat_id(
    session: Session,
    chat_id: UUID4,
    commit: bool = True,
) -> None:
    """Remove all messages by chat_id."""

    def _get_count(result) -> int | None:  # noqa: ANN001
        return getattr(result, "rowcount", None)

    query_seen_by = delete(MessageSeenBy).where(
        MessageSeenBy.message.has(
            MessageModel.chat_id == chat_id,
        )
    )
    result = session.exec(query_seen_by)
    events_logger.debug(f"Deleted {_get_count(result)=} seen_by records for chat_id={chat_id}.")
    query = delete(MessageModel).where(MessageModel.chat_id == chat_id)
    result = session.exec(query)
    events_logger.debug(f"Deleted {_get_count(result)=} messages for chat_id={chat_id}.")

    if commit:
        session.commit()


async def update_message(
    session: Session,
    message_id: UUID4,
    body: message_schema.MessageUpdate,
    current_user: AccountModel,
) -> MessageModel:
    """Update a message."""
    message_entity = session.get(MessageModel, message_id)

    if message_entity is None:
        raise SamuraiNotFoundError
    if message_entity.sender_id != current_user.account_id:
        raise SamuraiForbiddenError("You can only update your own messages.")

    message_entity.set_text(body.text)
    message_entity.file_id = body.file_id
    message_entity.update_time()

    session.add(message_entity)
    session.commit()

    await send_message_updated_ws_event(message_entity)

    return message_entity


async def mark_message_seen(
    session: Session,
    message_id: UUID4,
    current_user: AccountModel,
) -> tuple[MessageModel, MessageSeenBy | None]:
    """Mark a message as seen."""
    message_entity = session.get(MessageModel, message_id)

    if message_entity is None:
        raise SamuraiNotFoundError

    if message_entity.is_seen(current_user.account_id):
        return message_entity, None

    seen_by = message_entity.add_seen_by(current_user.account_id)

    session.add(message_entity)
    session.commit()

    await send_message_read_ws_event(message_entity, seen_by)

    return message_entity, seen_by


async def send_new_message_ws_event(
    message_entity: MessageModel,
) -> None:
    """Send a new message WebSocket event."""
    await web_socket_manager.broadcast(
        WSKeys.messages_key(message_entity.chat_id),
        MessageEvent(
            entity=message_entity,
            event_type="created",
        ),
    )


async def send_message_updated_ws_event(
    message_entity: MessageModel,
) -> None:
    """Send a message updated WebSocket event."""
    await web_socket_manager.broadcast(
        WSKeys.messages_key(message_entity.chat_id),
        MessageEvent(
            entity=message_entity,
            event_type="updated",
        ),
    )


async def send_message_read_ws_event(
    message_entity: MessageModel,
    seen_by: MessageSeenBy | None,
) -> None:
    """Send a message read WebSocket event."""
    if not seen_by:
        return

    await web_socket_manager.broadcast(
        WSKeys.messages_key(message_entity.chat_id),
        MessageEvent(
            entity=message_entity,
            seen_by=seen_by,
            event_type="read",
        ),
    )


async def send_typing_ws_event(
    chat_id: UUID4,
    current_user: AccountModel,
) -> None:
    """Send a typing WebSocket event."""
    await web_socket_manager.broadcast(
        WSKeys.messages_key(chat_id),
        MessageEvent(
            event_type="typing",
            typer=TyperData(
                account_id=current_user.account_id,
                chat_id=chat_id,
            ),
        ),
    )
