from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession

from common.filters.username_filter import UsernameFilter
from common.texts.user_texts import user_text

from database.sessions.user_session.order_session import orm_toggle_order_in_edit

from kbds.inline_kbds.user_inline_kbds import main_kbds

commands_router = Router()

@commands_router.callback_query(UsernameFilter())
@commands_router.message(UsernameFilter())
async def f_no_username(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text = user_text['no_username'])

@commands_router.message(Command('start'))
async def f_start_command(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await orm_toggle_order_in_edit(session=session, user_id=message.from_user.id)
    await message.answer(text = user_text['start'],
                         reply_markup = await main_kbds())

@commands_router.message(Command('help'))
async def f_help_command(message: Message):
    await message.answer(text = user_text['help_text'],
                         reply_markup = None)