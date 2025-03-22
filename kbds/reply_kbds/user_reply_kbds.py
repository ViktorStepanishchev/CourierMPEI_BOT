from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_send_phone():
    keyboard = [
        [
        KeyboardButton(
        text="📞 Отправить номер",
        request_contact=True)
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )