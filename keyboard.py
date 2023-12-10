from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers import openpyxl
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
def create():
    book = openpyxl.open("example.xlsx")
    sheet = book.active
    for row in range(1, 100):
        if not(sheet.cell(row=row, column=1).value is None):
                order_keyboard.button(text="Заказ #"+str(sheet.cell(row=row, column=1).value), callback_data='n'+str(sheet.cell(row=row, column=1).value))
    order_keyboard.adjust(1)