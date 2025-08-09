from aiogram import Router
from .callbacks import router as callback_router
from .messages import router as msg_router

router = Router()
router.include_routers(callback_router, msg_router)
