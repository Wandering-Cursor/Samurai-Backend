from pydantic.types import UUID4
from sqlmodel import delete

from samurai_backend.communication.schemas import message as message_schema
from samurai_backend.dependencies import account_type, database_session_type
from samurai_backend.errors import (
    SamuraiForbiddenError,
    SamuraiNotFoundError,
)
from samurai_backend.log import events_logger
from samurai_backend.models.communication.message import MessageModel, MessageSeenBy


async def create_message(
    session: database_session_type,
    create_message: message_schema.MessageCreate,
    current_user: account_type,
) -> MessageModel:
    """Create a message."""
    message_entity = MessageModel(
        chat_id=create_message.chat_id,
        sender_id=current_user.account_id,
        file_id=create_message.file_id,
    )
    message_entity.set_text(create_message.text)

    message_entity.add_seen_by(current_user.account_id)

    session.add(message_entity)
    session.commit()

    return message_entity


async def remove_all_messages_by_chat_id(
    session: database_session_type,
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
    session: database_session_type,
    message_id: UUID4,
    update_message: message_schema.MessageUpdate,
    current_user: account_type,
) -> MessageModel:
    """Update a message."""
    message_entity = session.get(MessageModel, message_id)

    if message_entity is None:
        raise SamuraiNotFoundError
    if message_entity.sender_id != current_user.account_id:
        raise SamuraiForbiddenError("You can only update your own messages.")

    message_entity.set_text(update_message.text)
    message_entity.file_id = update_message.file_id
    message_entity.update_time()

    session.add(message_entity)
    session.commit()

    return message_entity


async def mark_message_seen(
    session: database_session_type,
    message_id: UUID4,
    current_user: account_type,
) -> MessageModel:
    """Mark a message as seen."""
    message_entity = session.get(MessageModel, message_id)

    if message_entity is None:
        raise SamuraiNotFoundError

    if message_entity.is_seen(current_user.account_id):
        return message_entity

    message_entity.add_seen_by(current_user.account_id)

    session.add(message_entity)
    session.commit()

    return message_entity
