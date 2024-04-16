from typing import Annotated

from fastapi import Body, Depends

from samurai_backend.communication.operations import message as message_ops
from samurai_backend.communication.router import communication_router
from samurai_backend.communication.schemas import message as message_schema
from samurai_backend.dependencies import (
    account_type,
    database_session,
    database_session_type,
    get_current_active_account,
)
from samurai_backend.enums import Permissions


@communication_router.post(
    "/message",
    dependencies=[Permissions.MESSAGES_CREATE.as_security],
)
async def create_message(
    session: Annotated[database_session_type, Depends(database_session)],
    create_message: Annotated[message_schema.MessageCreate, Body()],
    current_user: Annotated[account_type, Depends(get_current_active_account)],
) -> message_schema.MessageRepresentation:
    """Create a message."""
    message_entity = await message_ops.create_message(
        session=session,
        create_message=create_message,
        current_user=current_user,
    )

    return message_schema.MessageRepresentation.model_validate(
        message_entity,
        from_attributes=True,
    )
