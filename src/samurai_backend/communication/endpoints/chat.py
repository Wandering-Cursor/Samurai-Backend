from typing import Annotated

import pydantic
from fastapi import Body, Depends

from samurai_backend.communication.get import chat as chat_get
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


@communication_router.get(
    "/chat",
    dependencies=[
        Permissions.CHATS_READ.as_security,
    ],
)
async def get_chats(
    session: Annotated[database_session_type, Depends(database_session)],
    current_user: Annotated[account_type, Depends(get_current_active_account)],
    search_params: Annotated[chat_schemas.ChatsSearchSchema, Depends()],
) -> chat_schemas.ChatsSearchResponse:
    """Get all chats that the user is a member of."""
    return await chat_get.get_user_chats(
        session=session,
        current_user=current_user,
        search_params=search_params,
    )


@communication_router.get(
    "/chat/{chat_id}",
    dependencies=[
        Permissions.CHATS_READ.as_security,
    ],
)
async def get_chat(
    session: Annotated[database_session_type, Depends(database_session)],
    chat_id: pydantic.UUID4,
    current_user: Annotated[account_type, Depends(get_current_active_account)],
) -> chat_schemas.ChatRepresentation:
    """Get a chat by its ID. If the user is not a member of the chat, raise 404."""
    chat_entity = await chat_get.get_related_chat(
        session=session,
        chat_id=chat_id,
        current_user=current_user,
    )

    return chat_schemas.ChatRepresentation.model_validate(
        chat_entity,
        from_attributes=True,
    )


@communication_router.patch(
    "/chat/{chat_id}",
    dependencies=[
        Permissions.CHATS_UPDATE.as_security,
    ],
)
async def update_chat(
    session: Annotated[database_session_type, Depends(database_session)],
    chat_id: pydantic.UUID4,
    chat_update: Annotated[chat_schemas.ChatUpdate, Body()],
    current_user: Annotated[account_type, Depends(get_current_active_account)],
) -> chat_schemas.ChatRepresentation:
    """Update a chat by its ID. If the user is not a member of the chat, raise 404."""
    chat = await chat_get.get_related_chat(
        session=session,
        chat_id=chat_id,
        current_user=current_user,
    )

    chat_entity = await chat_ops.update_chat(
        session=session,
        chat=chat,
        chat_update=chat_update,
    )

    return chat_schemas.ChatRepresentation.model_validate(
        chat_entity,
        from_attributes=True,
    )
