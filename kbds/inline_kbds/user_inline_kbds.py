from .gen_inline_kbds import get_callback_btns
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def main_kbds():
    main_kbds = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сделать заказ! 🛒️", callback_data="order"),
         InlineKeyboardButton(text = "Стать курьером! 🏃🏼‍", callback_data="courier")],

        [InlineKeyboardButton(text="Мой заказ 📦", callback_data="my_order")],

        [InlineKeyboardButton(text = "Помощь ⚙", callback_data="help")]
    ])
    return main_kbds

async def cancelled_create_order():
    btns = {
        "❌ Отмена": "back_to_main_menu",
    }
    return await get_callback_btns(btns=btns)