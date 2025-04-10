from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_send_phone():
    keyboard = [
        [KeyboardButton(text="📞 Отправить номер", request_contact=True)]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )

async def skip_kbds():
    keyboard = [
        [KeyboardButton(text='Пропустить')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )

async def edit_order_kbds():
    keyboard = [
        [KeyboardButton(text='Фото 📸'), KeyboardButton(text='Описание 🗒️')],
        [KeyboardButton(text='Удалить и заполнить заново 🔄')]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )