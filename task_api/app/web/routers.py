import typing
from app.tasks.routers import router as task_router
from app.auth.routers import router as auth_router
from app.internal.routers import router as interna_router

if typing.TYPE_CHECKING:
    from app.web.app import FastAPI


def setup_routers(app: "FastAPI"):
    app.include_router(task_router)
    app.include_router(auth_router)
    app.include_router(interna_router)
