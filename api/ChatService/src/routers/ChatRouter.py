from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.responses import HTMLResponse
from WebSocket.ConnManager import Manager
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import List, Dict


ChatRouter=APIRouter()


connections: Dict[str, List[WebSocket]] = {}

templates = Jinja2Templates(directory='templates')

@ChatRouter.get('/', response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


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
