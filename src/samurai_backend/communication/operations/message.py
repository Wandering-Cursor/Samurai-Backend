from samurai_backend.communication.schemas import message as message_schema
from samurai_backend.dependencies import account_type, database_session_type
from samurai_backend.models.communication.message import MessageModel


async def create_message(
    session: database_session_type,
    create_message: message_schema.MessageCreate,
    current_user: account_type,
) -> MessageModel:
    """Create a message."""
    message_entity = MessageModel(
        chat_id=create_message.chat_id,
        sender_id=current_user.account_id,
        text=create_message.text,
        file_id=create_message.file_id,
    )
    message_entity.add_seen_by(current_user.account_id)

    session.add(message_entity)
    session.commit()

    return message_entity
