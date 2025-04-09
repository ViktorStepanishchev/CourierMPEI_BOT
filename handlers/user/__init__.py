from aiogram import Router

from .commands_handler import commands_router
from handlers.user.order_handlers.create_order_handler import create_order_router
from handlers.user.order_handlers.my_order_handler import my_order_router
from handlers.user.order_handlers.help_handler import help_router
from handlers.user.order_handlers.edit_order_handler import edit_order_router
from handlers.user.courier_handlers import courier_router

from common.filters.chat_type_filter import ChatTypeFilter

user_router = Router()
user_router.message.filter(ChatTypeFilter(chat_type=['private']))

user_router.include_routers(commands_router,
                            create_order_router,
                            my_order_router,
                            help_router,
                            edit_order_router,
                            courier_router)