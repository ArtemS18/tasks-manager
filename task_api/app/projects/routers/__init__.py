from .projects import router
from .members import router as member_router
from .tasks import router as task_router
from .chat import router as chat_router

router.include_router(member_router)
router.include_router(task_router)
router.include_router(chat_router)
