import asyncio
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from database.sessions.user_session.order_session import (orm_get_customer_info,
                                                          orm_add_customer,
                                                          orm_get_costumer_attr)
from random import randint

from common.texts.user_texts import user_text
from common.states import CreateOrder
from kbds.reply_kbds.user_reply_kbds import (get_send_phone,
                                             skip_kbds)
from kbds.inline_kbds.user_inline_kbds import (order_is_done_kbds,
                                               main_kbds,
                                               to_main_menu_kbds,
                                               my_order_btns)

create_order_router = Router()

async def gen_order_id(session: AsyncSession):
    info = await orm_get_costumer_attr(session = session,
                                       attr = 'order_id')

    while True:
        order_id = randint(10000, 99999)
        if order_id not in info:
            return order_id

@create_order_router.callback_query(F.data == 'order')
async def f_start_create_order(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    customer_data = await orm_get_customer_info(session = session,
                                            user_id = callback.from_user.id)
    if customer_data is not None:
        order_id = customer_data.order_id
        await callback.message.edit_text(text = user_text['order_is_already_exists'].format(order_id),
                                reply_markup = await my_order_btns())
        return

    await state.update_data(order_user_id = callback.from_user.id)
    await state.update_data(order_username = callback.from_user.username)

    await state.set_state(CreateOrder.order_text)
    await callback.message.edit_text(text = user_text['order_text'],
                            reply_markup = None)

@create_order_router.message(CreateOrder.order_text, F.text)
async def f_get_order_text(message: Message, state: FSMContext):
    await state.update_data(order_text = message.text)

    await state.set_state(CreateOrder.order_photo)
    await message.answer(text = user_text['order_photo'],
                         reply_markup = await skip_kbds())

    await state.set_state(CreateOrder.order_photo)

@create_order_router.message(CreateOrder.order_photo, F.text == 'Пропустить')
async def f_get_order_photo_skip(message: Message, state: FSMContext):
    await state.update_data(order_photo=None)
    await state.set_state(CreateOrder.order_phone_number)

    await message.answer(text=user_text['order_phone_number'],
                         reply_markup=await get_send_phone())


@create_order_router.message(CreateOrder.order_photo, F.photo)
async def f_get_order_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(order_photo = photo)
    await state.set_state(CreateOrder.order_phone_number)

    await message.answer(text = user_text['order_phone_number'],
                         reply_markup = await get_send_phone())

@create_order_router.message(CreateOrder.order_phone_number, F.contact)
async def f_get_order_phone(message: Message, state: FSMContext, session: AsyncSession):
    order_id = await gen_order_id(session)
    await state.update_data(order_id = order_id)
    await state.update_data(order_phone_number = message.contact.phone_number)

    data = await state.get_data()

    if data['order_photo'] is not None:
        await message.answer_photo(photo=data['order_photo'],
                                   caption=user_text['my_order'].format(
                                       order_id = order_id,
                                       description = data['order_text'],
                                       phone_number = message.contact.phone_number,
                                       username = message.from_user.username,
                                   ),
                                   reply_markup= await order_is_done_kbds())
        return

    await message.answer(text = user_text['my_order'].format(
                                       order_id = order_id,
                                       description = data['order_text'],
                                       phone_number = message.contact.phone_number,
                                       username = message.from_user.username),
                             reply_markup=await order_is_done_kbds())

@create_order_router.callback_query(F.data == 'order_done')
async def f_order_is_created(callback:CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await state.clear()

    await orm_add_customer(session=session,
                           user_id=data['order_user_id'],
                           username=data['order_username'],
                           order_id=data['order_id'],
                           order_text=data['order_text'],
                           order_photo=data['order_photo'],
                           order_phone_number=data['order_phone_number'],)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(text = user_text['order_is_done'].format(order_id = data['order_id']))
    await asyncio.sleep(0.8)
    await callback.message.answer(text = user_text['start'],
                                  reply_markup=await main_kbds())

@create_order_router.callback_query(F.data == 'back_to_main_menu')
async def f_cancelled_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await callback.message.edit_text(text=user_text['start'],
                                         reply_markup=await main_kbds())
    except:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(text=user_text['start'],
                             reply_markup=await main_kbds())






