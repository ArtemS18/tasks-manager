from fastapi import WebSocket
from fastapi import status

from app.auth.schemas.users import User
from app.projects.schemas.chats import Message
from app.store.mongo.accessor import MongoAccessor

websockets: dict[int, set[WebSocket]] = {}
class ChatService:
    def __init__(self, mongo: MongoAccessor):
        self.mongo = mongo

    async def create_connection_to_project(self, ws: WebSocket, project_id: int):
        await ws.accept()
        project_ws = websockets.get(project_id, set())
        project_ws.add(ws)
        websockets[project_id] = project_ws
        await self.send_message_history(project_id, ws)

    async def send_message_history(self, project_id, ws):
        data = await self.mongo.get_messages(project_id)
        for ms in data:
            await self.send_message(ws, ms)

    async def close_connection(self, ws: WebSocket, project_id: int):
        try:
            if websockets[project_id]:
             websockets[project_id].remove(ws)
        except Exception as ex:
            pass
        finally:
            await ws.close(code=status.WS_1000_NORMAL_CLOSURE)

    async def send_message(self, ws: WebSocket, ms: Message):
        await ws.send_json(ms.model_dump_json())

    async def send_message_in_chat(self, ms: Message):
        await self.mongo.create_message(ms)
        for ws in websockets[ms.project_id]:
            await ws.send_json(ms.model_dump_json())
        

    

    