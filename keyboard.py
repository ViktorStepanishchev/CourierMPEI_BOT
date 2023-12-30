from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import back

main_keyboard = InlineKeyboardMarkup\
        (
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Сделать заказ! 🛒️", callback_data="order"),
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
                        InlineKeyboardButton(text="Удалить 🗑️", callback_data="delete_order")
                      ]
                    ]
        )

after_del_keyboard = InlineKeyboardMarkup\
        (
    inline_keyboard=[
                      [
                        InlineKeyboardButton(text = "Назад ↩", callback_data="back"),
                        InlineKeyboardButton(text="Сделать заказ! 🛒️", callback_data="order")
                      ]
                    ]
        )

get_order_keyboard = InlineKeyboardMarkup\
        (
    inline_keyboard=[
                      [
                        InlineKeyboardButton(text = "Назад ↩", callback_data="courier"),
                        InlineKeyboardButton(text="Взять заказ ✅", callback_data="get_order_clbck")
                      ]
                    ]
        )

order_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ↩", callback_data="back")]])
def add_inline_order_for_courier():
    order_keyboard.inline_keyboard.append([InlineKeyboardButton(text="Заказ #" + str(back.all_id_orders[-1]), callback_data=str(back.all_id_orders[-1]))])
def delete_inline_order_for_courier(num_iterat):
    order_keyboard.inline_keyboard.pop(num_iterat)