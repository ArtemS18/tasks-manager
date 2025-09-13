from typing import Annotated

from fastapi import Depends
from app.projects.services.chat import ChatService
from app.lib.fastapi import Request

def get_chat_service(req: Request):
    return ChatService(mongo=req.app.store.mongo)

ChatServiceDepend = Annotated[ChatService, Depends(get_chat_service)]