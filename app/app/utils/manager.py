from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import threading
from pydantic import BaseModel

# Class definitions
class Message(BaseModel):
    key: str
    value: str

class ConnectionManager:
    def __init__(self):
        self.available_connections: List[str] = []
        self.active_connections: dict[str] = {}
        self.active_pairs: dict[str] = {}
        self.lock = threading.Lock()

    async def connect(self, websocket: WebSocket, id: str):
        await websocket.accept()
        self.lock.acquire()
        self.active_connections[id] = websocket
        self.available_connections.append(id)
        self.lock.release()

    async def disconnect(self, websocket: WebSocket, id: str):
        self.lock.acquire()
        self.available_connections[id]
        self.available_connections.remove(id)
        self.active_connections.remove(websocket)
        self.lock.release()

    async def send_message(self, message: Message, websocket: WebSocket):
        try:
            await websocket.send_json(message)
            return (True, "Successfully sent message.")
        except Exception:
            return (False, "Error sending message. Please try again.")
        

    async def request_send_message(self, message: str, client_id: str):
        if (client_id in self.active_pairs):
            connection_id = self.active_pairs[client_id]
            if (connection_id in self.active_connections):
                connection = self.active_connections[connection_id]
                return await self.send_message(message, connection)
            else:
                return (False, "Connection was broken before message could be sent. Please reconnect.")
        else:
            return (False, "Active pair does not exist.")
        

    async def pair_client(self, client_id, connection_id):
        connection_id = str(connection_id)
        client_id = str(client_id)

        if (client_id in self.active_pairs):
            return (False, "Client is already connected to a robot.")

        # Critical section due to multiple server threads attempting to control a robot at the same time.
        if (connection_id not in self.available_connections):
            return (False, "Connection is not currently availble.")

        self.lock.acquire()
        self.active_pairs[client_id] = connection_id
        self.available_connections.remove(connection_id)
        self.lock.release()
        return (True, "Pairing was successful.")

    async def client_release_connection(self, client_id):
        if (client_id in self.active_pairs):
            self.lock.acquire()
            self.active_pairs.remove(client_id)
            self.available_connections.append(client_id)
            self.lock.release()

    def get_available_active_connections(self):
        return self.available_connections

    def get_all_active_connections(self):
        return self.active_connections.keys()

    def get_connection_by_client_id(self, client_id: str):
        client_id = str(client_id)
        if client_id in self.active_pairs:
            return self.active_pairs[client_id]
        else:
            return None

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()