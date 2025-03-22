from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

from common.filters.username_filter import UsernameFilter
from common.texts import user_text

from kbds.inline_kbds.user_inline_kbds import main_kbds

commands_router = Router()

@commands_router.message(UsernameFilter())
async def f_no_username(message: Message):
    await message.answer(text = user_text['no_username'],
                         reply_markup = None)

@commands_router.message(Command('start'))
async def f_start_command(message: Message):
    await message.answer(text = user_text['start'],
                         reply_markup = await main_kbds())

@commands_router.message(Command('help'))
async def f_help_command(message: Message):
    await message.answer(text = user_text['help_text'],
                         reply_markup = None)