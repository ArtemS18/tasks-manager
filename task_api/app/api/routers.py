import typing
from .tasks.endpoints import router as task_router
from .authorization.endpoints import router as autho_router
if typing.TYPE_CHECKING:
    from app.web.app import FastAPI

def setup_routers(app: "FastAPI"):
    app.include_router(task_router)
    app.include_router(autho_router)
    


