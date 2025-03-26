from aiogram import Router

from .commands_handler import commands_router
from .create_order_handler import create_order_router
from .my_order_handler import my_order_router

user_router = Router()

user_router.include_routers(commands_router,
                            create_order_router,
                            my_order_router)