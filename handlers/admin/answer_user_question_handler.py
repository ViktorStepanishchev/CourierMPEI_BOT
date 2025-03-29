from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from common.filters.username_filter import UsernameFilter
from common.states import AnswerMessageAdministration
from common.filters.chat_type_filter import ChatTypeFilter
from common.texts.admin_texts import admin_help_text
from common.texts.user_texts import user_text
from config import CHAT_ADMIN

answer_user_question_router = Router()

answer_user_question_router.message.filter(ChatTypeFilter(chat_type=['group', 'supergroup']))

@answer_user_question_router.callback_query(F.data.startswith('answer_user_question_'))
async def f_admin_press_button_for_answer_user_question(callback: CallbackQuery, state: FSMContext):
    question_data = callback.data.split("_")
    question_user_id, question_username = int(question_data[-2]), question_data[-1]

    await state.update_data(user_id=question_user_id)
    await state.update_data(user_username=question_username)
    await state.set_state(AnswerMessageAdministration.admin_msg_id)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text(text=admin_help_text['admin_answering_user'].format(admin_username=callback.from_user.username,
                                                                                         user_username=question_username))

@answer_user_question_router.message(AnswerMessageAdministration.admin_msg_id)
async def f_admin_answer_user_question(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id, user_username, admin_msg_id = data['user_id'], data['user_username'], message.message_id
    await state.clear()

    await message.bot.send_message(
        text=user_text['admin_answer'],
        chat_id=user_id,
    )

    await message.bot.copy_message(
        chat_id=user_id,
        from_chat_id=CHAT_ADMIN,
        message_id=admin_msg_id,
    )
    await message.answer(text=admin_help_text['admin_answer_user'].format(
        admin_username=message.from_user.username,
        user_username=user_username))
