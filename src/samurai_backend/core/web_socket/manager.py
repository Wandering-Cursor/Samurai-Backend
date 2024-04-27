from typing import TYPE_CHECKING

from fastapi import WebSocket, WebSocketDisconnect, WebSocketException

from samurai_backend.core.web_socket.types import WSError
from samurai_backend.log import main_logger

if TYPE_CHECKING:
    from pydantic import BaseModel


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[str, set[WebSocket]] = {}

    def _convert_to_dict(self, value: "BaseModel | dict") -> dict:
        if isinstance(value, dict):
            return value
        return value.model_dump(mode="json")

    async def connect(self, key: str, websocket: WebSocket) -> None:
        await websocket.accept()
        if key not in self.active_connections:
            self.active_connections[key] = set()
        self.active_connections[key].add(websocket)

    async def add_to_key(self, key: str, websocket: WebSocket) -> None:
        if key not in self.active_connections:
            self.active_connections[key] = set()
        self.active_connections[key].add(websocket)

    async def disconnect(self, key: str, websocket: WebSocket) -> None:
        self.active_connections[key].remove(websocket)
        try:
            await websocket.send_json({"message": "disconnected"})
            await websocket.close()
        except (WebSocketException, WebSocketDisconnect, Exception) as e:
            main_logger.error("Disconnect error", extra={"error": e}, exc_info=True)

    async def send_personal_message(
        self,
        websocket: WebSocket,
        message: "BaseModel | dict",
    ) -> None:
        message = self._convert_to_dict(message)

        await websocket.send_json(message)

    async def invalid_command(
        self,
        websocket: WebSocket,
        error: dict | str,
    ) -> None:
        await self.send_personal_message(
            websocket,
            WSError(
                error="Invalid data",
                message=error,
            ),
        )

    async def broadcast(
        self,
        key: str,
        message: "BaseModel | dict",
    ) -> None:
        message = self._convert_to_dict(message)

        if key in self.active_connections:
            for connection in self.active_connections[key]:
                await connection.send_json(message)


web_socket_manager = ConnectionManager()
