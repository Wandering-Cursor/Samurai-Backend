from typing import Annotated

import pydantic
from fastapi import BackgroundTasks, Body, Depends

from samurai_backend.communication.get import chat as chat_get
from samurai_backend.communication.operations import chat as chat_ops
from samurai_backend.communication.router import communication_router
from samurai_backend.communication.schemas import chat as chat_schemas
from samurai_backend.db import get_db_session_async
from samurai_backend.dependencies.get_current_active_account import get_current_active_account
from samurai_backend.enums.permissions import Permissions
from samurai_backend.models.account.account import AccountModel


@communication_router.post(
    "/chat",
    dependencies=[
        Permissions.CHATS_CREATE.as_security,
    ],
)
async def create_chat(
    session: Annotated[get_db_session_async, Depends(get_db_session_async)],
    body: Annotated[chat_schemas.ChatCreate, Body()],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
) -> chat_schemas.ChatRepresentation:
    """Create a chat with (or without) some users."""
    chat_entity = await chat_ops.create_chat(
        session=session,
        body=body,
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
    session: Annotated[get_db_session_async, Depends(get_db_session_async)],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
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
    session: Annotated[get_db_session_async, Depends(get_db_session_async)],
    chat_id: pydantic.UUID4,
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
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


@communication_router.get(
    "/chat/{chat_id}/participants",
    dependencies=[
        Permissions.CHATS_READ.as_security,
    ],
)
async def get_chat_participants(
    session: Annotated[get_db_session_async, Depends(get_db_session_async)],
    chat_id: pydantic.UUID4,
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
    search_schema: Annotated[chat_schemas.ChatsSearchSchema, Depends()],
) -> chat_schemas.ChatParticipantsResponse:
    """
    Get all participants of a chat by its ID. If the user is not a member of the chat, raise 404.
    """
    chat_entity = await chat_get.get_related_chat(
        session=session,
        chat_id=chat_id,
        current_user=current_user,
    )

    return await chat_get.get_chat_participants(
        session=session,
        chat=chat_entity,
        search_schema=search_schema,
    )


@communication_router.patch(
    "/chat/{chat_id}",
    dependencies=[
        Permissions.CHATS_UPDATE.as_security,
    ],
)
async def update_chat(
    session: Annotated[get_db_session_async, Depends(get_db_session_async)],
    chat_id: pydantic.UUID4,
    chat_update: Annotated[chat_schemas.ChatUpdate, Body()],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
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


@communication_router.post(
    "/chat/{chat_id}/add_member",
    dependencies=[
        Permissions.CHATS_ADD_MEMBER.as_security,
    ],
)
async def add_chat_member(
    session: Annotated[get_db_session_async, Depends(get_db_session_async)],
    chat_id: pydantic.UUID4,
    add_member_input: Annotated[chat_schemas.ChatAddMember, Body()],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
) -> chat_schemas.ChatRepresentation:
    """
    Add a member to a chat by its ID. If the user is not a member of the chat, raise 404.
    Duplicates will be ignored, and if the user does not exist, it will be ignored.
    """
    chat_entity = await chat_get.get_related_chat(
        session=session,
        chat_id=chat_id,
        current_user=current_user,
    )

    chat_entity = await chat_ops.add_chat_member(
        session=session,
        chat=chat_entity,
        add_member_input=add_member_input,
    )

    return chat_schemas.ChatRepresentation.model_validate(
        chat_entity,
        from_attributes=True,
    )


@communication_router.post(
    "/chat/{chat_id}/leave",
)
async def leave_chat(
    session: Annotated[get_db_session_async, Depends(get_db_session_async)],
    chat_id: pydantic.UUID4,
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
    background_tasks: BackgroundTasks,
) -> chat_schemas.ChatLeaveResponse:
    """Leave a chat by its ID. If the user is not a member of the chat, raise 404."""
    chat_entity = await chat_get.get_related_chat(
        session=session,
        chat_id=chat_id,
        current_user=current_user,
    )

    left = await chat_ops.leave_chat(
        session=session,
        chat=chat_entity,
        account=current_user,
    )

    if left:
        background_tasks.add_task(
            chat_ops.remove_empty_chat,
            session=get_db_session_async(),
            chat_id=chat_entity.chat_id,
        )

    return chat_schemas.ChatLeaveResponse(
        left=left,
    )
