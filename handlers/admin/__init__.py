from aiogram import Router

from .answer_user_question_handler import answer_user_question_router

admin_router = Router()
admin_router.include_router(answer_user_question_router)