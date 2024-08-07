from typing import List, Dict
from fastapi import WebSocket

from db.Redis.Sessions import Sessions

from Settings.RedisSettings import redisSettings

class ConnectionManager():

    def __init__(self)->None:
        self.ActiveConnections: Dict[str, List[WebSocket]] = {} 


    async def connect(self, websocket: WebSocket, uuid: str)->None:
        await websocket.accept()
        if uuid not in self.ActiveConnections:
            self.ActiveConnections[uuid] = []

        self.ActiveConnections[uuid].append(websocket)


    async def disconnect(self, websocket: WebSocket, uuid)->None:
        self.ActiveConnections[uuid].remove(websocket)
        if not self.ActiveConnections[uuid]:  # Удаляем чат, если больше нет подключений
            del self.ActiveConnections[uuid]


    async def broadcast(self, message: str | int, uuid:str)->None:
        for data in self.ActiveConnections[uuid]:
            await data.send_text(message)

Manager = ConnectionManager()