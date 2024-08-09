from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.responses import HTMLResponse
from WebSocket.ConnManager import Manager

ChatRouter=APIRouter()


@ChatRouter.websocket('/chat/{chat_id}')
async def chat(
    websocket: WebSocket, chat_id: str
)->None:
    await Manager.connect(websocket=websocket, uuid=chat_id)
    try:
        while True:
            data = await websocket.receive_text()
            await Manager.broadcast(message=f'{data}', uuid=chat_id)
    except WebSocketDisconnect:
        await Manager.disconnect(websocket=websocket, uuid=chat_id)
