from aiogram import Router


from .user import user_router

router = Router()

router.include_router(user_router)
