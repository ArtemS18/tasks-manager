from app.base.accessor import BaseAccessor
from app.lib.fastapi import FastAPI 
from motor.motor_asyncio import AsyncIOMotorClient
from app.projects.schemas.chats import Message


class MongoAccessor(BaseAccessor):
    def __init__(self, app: "FastAPI"):
        super().__init__(app)
        self.client: AsyncIOMotorClient =  None
    async def connect(self):
        self.client = AsyncIOMotorClient(
            self.app.config.mongo.url
        )
        self.db = self.client[self.app.config.mongo.db] 

    async def disconnect(self):
        if self.client:
            self.client.close()

    async def create_message(self, ms: Message) -> int:
        new_ms = await self.db.messages.insert_one(ms.model_dump(by_alias=True, exclude_none=False, exclude={"id"}))
        return new_ms.inserted_id
    
    async def get_messages(self, project_id: int) -> list:
        raw_messages = self.db.messages.find({"project_id": project_id})
        messages = await raw_messages.to_list(length=None)
        print(messages)
        obj_ms = [Message.model_validate(ms) for ms in messages]
        return obj_ms
    
    
    
