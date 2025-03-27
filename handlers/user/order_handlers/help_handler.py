from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from config import CHAT_ADMIN

from common.texts.user_texts import user_text
from common.texts.admin_texts import admin_help_text
from common.states import MessageToAdministration
from database.sessions.admin_session.msg_to_admin_session import orm_add_user_msg
from kbds.inline_kbds.user_inline_kbds import (help_kbds,
                                               to_main_menu_kbds)
from kbds.inline_kbds.admin_inline_kbds import answer_user_question

help_router = Router()

@help_router.callback_query(F.data == 'help')
async def f_help_handler(callback: CallbackQuery):
    await callback.message.edit_text(text=user_text['help_text'],
                                     reply_markup=await help_kbds())

@help_router.callback_query(F.data == 'admin_call')
async def f_admin_call(callback: CallbackQuery, state: FSMContext):

    await state.update_data(username = callback.from_user.username)
    await state.set_state(MessageToAdministration.msg_id)

    await callback.message.edit_text(text=user_text['admin_call'],
                                     reply_markup=await to_main_menu_kbds())

@help_router.message(MessageToAdministration.msg_id)
async def f_send_admin_message(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(msg_id = message.message_id)
    data = await state.get_data()
    await state.clear()

    await orm_add_user_msg(session=session,
                           user_id=message.from_user.id,
                           username=message.from_user.username,
                           msg_id=data['msg_id'])

    await message.bot.send_message(chat_id=CHAT_ADMIN,
                                   text=admin_help_text['user_have_a_question'].format(
                                       username = message.from_user.username),
                                   reply_markup=await answer_user_question(user_id=message.from_user.id,
                                                                           username=message.from_user.username))
    await message.bot.forward_message(chat_id=CHAT_ADMIN,
                                      from_chat_id=message.from_user.id,
                                      message_id = message.message_id)

