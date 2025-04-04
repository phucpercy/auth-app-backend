from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Set
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Store active connections
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        logger.info("connecting user:" + str(user_id))
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected. Total connections: {self._count_connections()}")

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"User {user_id} disconnected. Total connections: {self._count_connections()}")

    async def broadcast(self, message: dict, exclude_user: int = None):
        logger.info(f"Broadcasting message to {self._count_connections(exclude_user)} users")
        for user_id, connections in self.active_connections.items():
            if user_id != exclude_user:
                for connection in connections:
                    try:
                        await connection.send_json(message)
                    except Exception as e:
                        logger.error(f"Error sending message to user {user_id}: {e}")

    def _count_connections(self, exclude_user: int = None) -> int:
        count = 0
        for user_id, connections in self.active_connections.items():
            if user_id != exclude_user:
                count += len(connections)
        return count

# Create a global instance
manager = ConnectionManager()