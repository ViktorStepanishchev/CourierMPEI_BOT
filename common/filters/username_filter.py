from aiogram.filters import Filter
from aiogram.types import Message

class UsernameFilter(Filter):
    async def __call__(self, message: Message):
        if message.from_user.username is None: return True