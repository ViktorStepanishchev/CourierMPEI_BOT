from aiogram import Router
from .view_take_order_handler import view_take_order_router

courier_router = Router()
courier_router.include_router(view_take_order_router)