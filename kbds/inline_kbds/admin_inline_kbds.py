from .gen_inline_kbds import get_callback_btns
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def answer_user_question_kbds(user_id: int,
                                    username: str):
    btns = {
        f"Ответить @{username}": f"answer_user_question_{user_id}_{username}"
    }
    return await get_callback_btns(btns=btns)