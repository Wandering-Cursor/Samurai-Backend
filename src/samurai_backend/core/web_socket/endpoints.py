import uuid
from typing import Annotated

import pydantic
from fastapi import Depends, Security, WebSocket, WebSocketDisconnect, WebSocketException

from samurai_backend.communication.get.chat import get_related_chat
from samurai_backend.communication.operations.message import mark_message_seen, send_typing_ws_event
from samurai_backend.core.router import ws_router
from samurai_backend.core.web_socket.manager import web_socket_manager
from samurai_backend.core.web_socket.types import (
    ConnectedResponse,
    WebSocketCommand,
    WSError,
    WSKeys,
)
from samurai_backend.dependencies import (
    account_type,
    database_session,
    database_session_type,
    ws_get_current_active_account,
)
from samurai_backend.enums import Permissions
from samurai_backend.log import events_logger


@ws_router.websocket(
    "/chats",
    name="Chat list websocket",
)
async def chats_list_endpoint(
    websocket: WebSocket,
    account: Annotated[
        account_type,
        Security(
            ws_get_current_active_account,
            scopes=[Permissions.CHATS_READ.value],
        ),
    ],
) -> None:
    key = WSKeys.chats_key(account.account_id)

    await web_socket_manager.connect(key, websocket)
    await web_socket_manager.send_personal_message(
        websocket,
        ConnectedResponse(commands=["bye"]),
    )
    try:
        while True:
            data = await websocket.receive_json()

            try:
                data = WebSocketCommand(**data)
            except pydantic.ValidationError as e:
                events_logger.info("Invalid data", extra={"data": e.json()})
                await web_socket_manager.send_personal_message(
                    websocket,
                    WSError(
                        error="Invalid data",
                        message=e.json(),
                    ),
                )
                continue

            if data.action == "bye":
                await web_socket_manager.disconnect(key, websocket)
                break

            await web_socket_manager.invalid_command(
                websocket,
                "Invalid action",
            )
    except (WebSocketDisconnect, WebSocketException):
        web_socket_manager.disconnect(key, websocket)


@ws_router.websocket(
    "/messages/{chat_id}",
    name="Chat messages websocket",
)
async def chats_messages_endpoint(
    websocket: WebSocket,
    account: Annotated[
        account_type,
        Security(
            ws_get_current_active_account,
            scopes=[Permissions.CHATS_READ.value],
        ),
    ],
    chat_id: pydantic.UUID4,
    session: Annotated[database_session_type, Depends(database_session)],
) -> None:
    # Raises NotFoundException if chat is not found
    await get_related_chat(
        session=session,
        chat_id=chat_id,
        current_user=account,
    )

    key = WSKeys.messages_key(chat_id)
    await web_socket_manager.connect(key, websocket)
    await web_socket_manager.send_personal_message(
        websocket,
        ConnectedResponse(commands=["typing", "mark_as_read", "bye"]),
    )

    try:
        while True:
            data = await websocket.receive_json()

            try:
                data = WebSocketCommand(**data)
            except pydantic.ValidationError as e:
                await web_socket_manager.send_personal_message(
                    websocket,
                    WSError(
                        error="Invalid data",
                        message=e.json(),
                    ),
                )
                continue

            if data.action == "bye":
                await web_socket_manager.disconnect(key, websocket)
                break
            if data.action == "typing":
                await send_typing_ws_event(
                    chat_id=chat_id,
                    current_user=account,
                )
                continue
            if data.action == "mark_as_read":
                if not isinstance(data.data, dict) or "message_id" not in data.data:
                    await web_socket_manager.invalid_command(websocket, "message_id is required")
                    continue

                try:
                    message_id = uuid.UUID(data.data["message_id"])
                except (ValueError, AttributeError, Exception) as e:
                    events_logger.error("Invalid message_id", exc_info=True, extra={"data": e})
                    await web_socket_manager.invalid_command(websocket, "Invalid message_id")
                    continue

                await mark_message_seen(
                    session=session,
                    message_id=message_id,
                    current_user=account,
                )
                continue

            await web_socket_manager.invalid_command(
                websocket,
                "Invalid action",
            )
    except (WebSocketDisconnect, WebSocketException):
        web_socket_manager.disconnect(key, websocket)
