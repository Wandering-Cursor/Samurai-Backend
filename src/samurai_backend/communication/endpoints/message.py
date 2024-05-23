from typing import Annotated

import pydantic
from fastapi import Body, Depends
from sqlmodel import Session

from samurai_backend.communication.get import message as message_get
from samurai_backend.communication.get.chat import get_related_chat
from samurai_backend.communication.operations import message as message_ops
from samurai_backend.communication.router import communication_router
from samurai_backend.communication.schemas import message as message_schema
from samurai_backend.db import get_db_session_async
from samurai_backend.dependencies.get_current_active_account import get_current_active_account
from samurai_backend.enums.permissions import Permissions
from samurai_backend.errors import SamuraiNotFoundError
from samurai_backend.models.account.account import AccountModel


@communication_router.get(
    "/messages",
    dependencies=[Permissions.MESSAGES_READ.as_security],
)
async def get_messages(
    session: Annotated[Session, Depends(get_db_session_async)],
    search_schema: Annotated[message_schema.MessagesSearchSchema, Depends()],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
) -> message_schema.MessagesSearchResponse:
    """Get messages."""
    # Raises exception if chat does not exist or user is not a member
    await get_related_chat(
        session=session,
        chat_id=search_schema.chat_id,
        current_user=current_user,
    )

    return await message_get.get_messages(
        session=session,
        search_schema=search_schema,
    )


@communication_router.get(
    "/message/{message_id}",
    dependencies=[Permissions.MESSAGES_READ.as_security],
)
async def get_message(
    message_id: pydantic.UUID4,
    session: Annotated[Session, Depends(get_db_session_async)],
) -> message_schema.MessageRepresentation:
    """Get a message."""
    message_entity = await message_get.get_message(
        session=session,
        message_id=message_id,
    )

    if message_entity is None:
        raise SamuraiNotFoundError

    return message_schema.MessageRepresentation.model_validate(
        message_entity,
        from_attributes=True,
    )


@communication_router.get(
    "/message/{message_id}/seen_by",
    dependencies=[Permissions.MESSAGES_READ.as_security],
)
async def get_message_seen_by(
    message_id: pydantic.UUID4,
    session: Annotated[Session, Depends(get_db_session_async)],
) -> message_schema.MessageSeenByResponse:
    """Get message seen by."""
    message_entity = await message_get.get_message(
        session=session,
        message_id=message_id,
    )

    if message_entity is None:
        raise SamuraiNotFoundError

    return message_schema.MessageSeenByResponse.from_seen_by(message_entity.seen_by)


@communication_router.post(
    "/message",
    dependencies=[Permissions.MESSAGES_CREATE.as_security],
    status_code=201,
)
async def create_message(
    session: Annotated[Session, Depends(get_db_session_async)],
    body: Annotated[message_schema.MessageCreate, Body()],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
) -> message_schema.MessageRepresentation:
    """Create a message."""
    message_entity = await message_ops.create_message(
        session=session,
        body=body,
        current_user=current_user,
    )

    return message_schema.MessageRepresentation.model_validate(
        message_entity,
        from_attributes=True,
    )


@communication_router.put(
    "/message/{message_id}",
    dependencies=[Permissions.MESSAGES_UPDATE.as_security],
)
async def update_message(
    message_id: pydantic.UUID4,
    session: Annotated[Session, Depends(get_db_session_async)],
    update_message: Annotated[message_schema.MessageUpdate, Body()],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
) -> message_schema.MessageRepresentation:
    """Update a message."""
    message_entity = await message_ops.update_message(
        session=session,
        message_id=message_id,
        body=update_message,
        current_user=current_user,
    )

    return message_schema.MessageRepresentation.model_validate(
        message_entity,
        from_attributes=True,
    )


@communication_router.patch(
    "/message/{message_id}/seen",
    dependencies=[Permissions.MESSAGES_UPDATE.as_security],
    status_code=204,
)
async def mark_message_seen(
    message_id: pydantic.UUID4,
    session: Annotated[Session, Depends(get_db_session_async)],
    current_user: Annotated[AccountModel, Depends(get_current_active_account)],
) -> None:
    """Mark message as seen."""
    await message_ops.mark_message_seen(
        session=session,
        message_id=message_id,
        current_user=current_user,
    )
