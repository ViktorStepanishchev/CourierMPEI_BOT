from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_keyboard = InlineKeyboardMarkup\
        (
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Сделать заказ! 🗳️", callback_data="order"),
            InlineKeyboardButton(text = "Стать курьером! 🏃🏼‍", callback_data="courier")
        ],
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

order_keyboard = InlineKeyboardBuilder()
order_keyboard.button(text="Назад ↩", callback_data="back")
def create(orders):
    for i in range(len(orders)):
        print(orders[i][0])
        order_keyboard.button(text = "Заказ #"+orders[i][0], callback_data=('n'+orders[i][0]))
    order_keyboard.adjust(1)