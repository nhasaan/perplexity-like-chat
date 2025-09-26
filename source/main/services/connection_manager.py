from fastapi import WebSocket
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            try:
                await websocket.send_text(message)
            except:
                # Connection might be closed, remove it
                self.disconnect(client_id)

    async def broadcast(self, message: str):
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(message)
            except:
                # Remove broken connections
                self.disconnect(client_id)

    def get_active_connections(self) -> List[str]:
        return list(self.active_connections.keys())
