from samurai_backend.account.get.account import get_account_by_id
from samurai_backend.communication.schemas import chat as chat_schemas
from samurai_backend.dependencies import account_type, database_session_type
from samurai_backend.models.communication.chat import ChatModel


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
