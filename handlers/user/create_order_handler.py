from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from database.sessions.user_session.order_session import (orm_get_customer_info,
                                                          orm_add_customer)

from common.texts import user_text
from common.states import CreateOrder
from kbds.reply_kbds.user_reply_kbds import get_send_phone

create_order_router = Router()

@create_order_router.callback_query(F.data == 'order')
async def f_start_create_order(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    customer_data = await orm_get_customer_info(session = session,
                                            user_id = callback.from_user.id)
    if customer_data is not None:
        order_id = customer_data.order_id
        await callback.message.edit_text(text = user_text['order_is_already_exists'].format(order_id),
                                reply_markup=ReplyKeyboardRemove())
        return

    await state.set_state(CreateOrder.order_text)
    await callback.message.edit_text(text = user_text['order_text'],
                            reply_markup = None)

@create_order_router.message(CreateOrder.order_text, F.text)
async def f_get_order_text(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(order_text = message.text)

    await state.set_state(CreateOrder.order_photo)
    await message.answer(text = user_text['order_photo'],
                         reply_markup = None)

    await state.set_state(CreateOrder.order_photo)

@create_order_router.message(CreateOrder.order_photo, F.photo)
async def f_get_order_photo(message: Message, state: FSMContext, session: AsyncSession):
    photo = message.photo[-1].file_id
    data = await state.get_data()

    await orm_add_customer(session = session,
                           user_id = data.get('user_id'),
                           username = message.from_user.username,
                           order_id = 12345)
