import typing
from app.auth.routers import router as auth_router
from app.internal.routers import router as interna_router
from app.projects.routers import router as project_router
from app.websocket.routers import router as websocket_router

if typing.TYPE_CHECKING:
    from app.web.app import FastAPI


def setup_routers(app: "FastAPI"):
    app.include_router(project_router)
    app.include_router(auth_router)
    app.include_router(websocket_router)
    app.include_router(interna_router)
