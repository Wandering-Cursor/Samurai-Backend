from typing import Annotated

from fastapi import Body, Depends

from samurai_backend.communication.operations import chat as chat_ops
from samurai_backend.communication.router import communication_router
from samurai_backend.communication.schemas import chat as chat_schemas
from samurai_backend.dependencies import (
    account_type,
    database_session,
    database_session_type,
    get_current_active_account,
)
from samurai_backend.enums import Permissions


@communication_router.post(
    "/chat",
    dependencies=[
        Permissions.CHATS_CREATE.as_security,
    ],
)
async def create_chat(
    session: Annotated[database_session_type, Depends(database_session)],
    create_chat: Annotated[chat_schemas.ChatCreate, Body()],
    current_user: Annotated[account_type, Depends(get_current_active_account)],
) -> chat_schemas.ChatRepresentation:
    """Create a chat with (or without) some users."""
    chat_entity = await chat_ops.create_chat(
        session=session,
        create_chat=create_chat,
        current_user=current_user,
    )

    return chat_schemas.ChatRepresentation.model_validate(
        chat_entity,
        from_attributes=True,
    )
