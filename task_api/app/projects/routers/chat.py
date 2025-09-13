from datetime import datetime
import os

from fastapi.templating import Jinja2Templates

from app.auth.schemas.users import User
from app.projects.depends.chat import ChatServiceDepend
from app.projects.schemas.chats import Message
from fastapi import APIRouter, Depends, WebSocketDisconnect
from app.projects.depends.validate import validation_access_token
from app.lib.fastapi import Request, WebSocket
from app.projects.services.chat import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

BASE_DIR = "app/projects/templates"

templates = Jinja2Templates(directory=BASE_DIR)

@router.get("/{project_id}/")
async def get_page(req: Request, project_id: int):
    return templates.TemplateResponse(req, "template.html", {
        "project_id": project_id
    })


@router.websocket("/{project_id}/ws")
async def websocket_handel(
    ws: WebSocket, 
    project_id: int,
    #user: User=Depends(validation_access_token),
    
):
    chat_service= ChatService(mongo=ws.app.store.mongo)
    await chat_service.create_connection_to_project(ws, project_id)
    try:
        while True:
            text = await ws.receive_text()
            print(text)
            new_ms=Message(
                text=text,
                author=User(id=1, login="user1@gmail.com", name="User1"),
                project_id=project_id,
                chat_id=1
            )
            await chat_service.send_message_in_chat(new_ms)
    except WebSocketDisconnect:
        pass
    finally:
        await chat_service.close_connection(ws, project_id)

          
