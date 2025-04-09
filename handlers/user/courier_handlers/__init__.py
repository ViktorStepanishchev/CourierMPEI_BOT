from aiogram import Router
from .reg_courier import view_orders_router

courier_router = Router()
courier_router.include_router(view_orders_router)