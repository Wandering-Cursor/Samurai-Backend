from typing import TYPE_CHECKING

from fastapi import WebSocket

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
        await websocket.send_json({"message": "disconnected"})
        await websocket.close()

    async def send_personal_message(
        self,
        websocket: WebSocket,
        message: "BaseModel | dict",
    ) -> None:
        message = self._convert_to_dict(message)

        await websocket.send_json(message)

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
