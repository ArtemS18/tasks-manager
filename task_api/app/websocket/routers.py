from datetime import datetime
import os
from fastapi import APIRouter, WebSocket
from fastapi.responses import FileResponse, HTMLResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@router.get("/")
async def get_page():
    return FileResponse(os.path.join(BASE_DIR, "template.html"))


@router.websocket("/ws")
async def websocket_handel(ws: WebSocket):
    await ws.accept()
    while True:
        message = await ws.receive_text()
        await ws.send_json(
            data={
                "user": "You",
                "message": f"{message}",
                "data": str(datetime.now()),
            }
        )
