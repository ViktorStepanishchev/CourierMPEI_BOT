from aiogram import Router

from .commands_handler import commands_router
from handlers.user.order_handlers.create_order_handler import create_order_router
from handlers.user.order_handlers.my_order_handler import my_order_router
from handlers.user.order_handlers.help_handler import help_router

user_router = Router()

user_router.include_routers(commands_router,
                            create_order_router,
                            my_order_router,
                            help_router)