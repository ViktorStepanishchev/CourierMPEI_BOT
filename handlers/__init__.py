from aiogram import Router

from .user import user_router
from .admin import admin_router

router = Router()

router.include_routers(user_router,
                      admin_router)
