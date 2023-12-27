from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import back

main_keyboard = InlineKeyboardMarkup\
        (
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Сделать заказ! 🗳️", callback_data="order"),
            InlineKeyboardButton(text = "Стать курьером! 🏃🏼‍", callback_data="courier")
        ],
        [
            InlineKeyboardButton(text="Мой заказ 📦", callback_data="my_order"),
        ]
        ,
        [
            InlineKeyboardButton(text = "Помощь ⚙", callback_data="help"),
        ]
    ]
        )

help_keyboard = InlineKeyboardMarkup\
        (
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Поддержка 🕴", url = "tg://resolve?domain=byvs000"),
        ],
        [
            InlineKeyboardButton(text = "Назад ↩", callback_data="back"),
        ]
    ]
        )

back_keyboard = InlineKeyboardMarkup\
        (
    inline_keyboard=[[InlineKeyboardButton(text = "Назад ↩", callback_data="back")]]
        )

back_to_orders_keyboard = InlineKeyboardMarkup\
        (
    inline_keyboard=[[InlineKeyboardButton(text = "Назад ↩", callback_data="courier")]]
        )

del_keyboard = InlineKeyboardMarkup\
        (
    inline_keyboard=[
                      [
                        InlineKeyboardButton(text = "Назад ↩", callback_data="back"),
                        InlineKeyboardButton(text="Редактировать 🔧", callback_data="red_order")
                      ]
                    ]
        )

order_keyboard = InlineKeyboardBuilder()
order_keyboard.button(text="Назад ↩", callback_data="back")
def add_inline_order_for_courier():
    order_keyboard.button(text="Заказ #" + str(back.all_id_orders[-1]), callback_data=str(back.all_id_orders[-1]))
    order_keyboard.adjust(1)