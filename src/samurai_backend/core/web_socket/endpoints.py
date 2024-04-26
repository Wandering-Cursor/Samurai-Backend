from typing import Annotated

import pydantic
from fastapi import Security, WebSocket, WebSocketDisconnect, WebSocketException

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
    ws_get_current_active_account,
)
from samurai_backend.enums import Permissions


@ws_router.websocket(
    "/chats",
    name="Chat list websocket",
)
async def websocket_endpoint(
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

            await web_socket_manager.send_personal_message(
                websocket,
                WSError(
                    error="Invalid action",
                    message="Invalid action",
                ),
            )
    except (WebSocketDisconnect, WebSocketException):
        web_socket_manager.disconnect(key, websocket)
