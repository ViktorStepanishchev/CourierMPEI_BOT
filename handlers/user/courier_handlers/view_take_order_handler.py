from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from common.texts.user_texts import courier_text, user_text
from common.filters.order_in_edit_or_deleted_filter import OrderInEditOrDeletedFilter
from common.states import CourierStates
from database.sessions.user_session.courier_session import orm_update_courier, orm_add_courier
from kbds.inline_kbds.user_inline_kbds import orders_kbds, to_main_menu_kbds
from kbds.inline_kbds.user_inline_kbds import take_order_kbds
from database.sessions.user_session.order_session import (orm_get_order,
                                                          orm_get_costumer_attr,
                                                          orm_update_customer_info)
from kbds.reply_kbds.user_reply_kbds import get_send_phone

view_take_order_router = Router()

@view_take_order_router.callback_query(F.data.startswith('courier_'))
async def f_view_orders(callback: CallbackQuery, session: AsyncSession):
    callback_data = callback.data.split("_")[-1]
    if callback_data == '0': page=0
    else: page = int(callback_data)

    orders_list = await orm_get_costumer_attr(session=session,
                                                   attr='order_id')
    all_pages = int(len(orders_list) / 5)
    try:
        await callback.message.edit_text(text=courier_text['view_orders'].format(page=int(page/5)+1, len_pages=all_pages),
                                         reply_markup = await orders_kbds(session, page))
    except:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(text=courier_text['view_orders'].format(page=page, len_pages=all_pages),
                                      reply_markup = await orders_kbds(session, page))

@view_take_order_router.callback_query(OrderInEditOrDeletedFilter())
async def f_order_is_edit_or_deleted(callback: CallbackQuery, session: AsyncSession):
    page = int(callback.data.split("_")[-1])
    await callback.answer(text='Этот заказ сейчас недоступен')
    try:
        await callback.message.edit_reply_markup(reply_markup=await orders_kbds(session, page))
    except:
        pass

@view_take_order_router.callback_query(F.data.startswith('order_'))
async def f_view_order(callback: CallbackQuery, session: AsyncSession):
    callback_data = callback.data.split("_")
    order_id = int(callback_data[-2])
    page = int(callback_data[-1])
    order_data = await orm_get_order(session=session, order_id=order_id)
    view_order_text = courier_text['view_order_first_info'].format(order_id=order_data.order_id,
                                                                description=order_data.order_text)
    if order_data.order_photo:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer_photo(photo=order_data.order_photo,
                                            caption=view_order_text,
                                            reply_markup = await take_order_kbds(order_id=order_id,
                                                                                 page=page))
        return
    await callback.message.edit_text(text=view_order_text,
                                     reply_markup = await take_order_kbds(order_id=order_id,
                                                                                 page=page))

@view_take_order_router.callback_query(F.data.startswith('take_order_'))
async def f_take_order(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    callback_data = callback.data.split('_')
    order_id = int(callback_data[-2])
    await state.update_data(order_id=order_id)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(text = user_text["courier_phone_number"],
                                  reply_markup = await get_send_phone())
    await state.set_state(CourierStates.waiting_for_phone)

@view_take_order_router.message(CourierStates.waiting_for_phone, F.contact)
async def f_send_phone_number_by_courier(message: Message, state: FSMContext, session: AsyncSession):
    courier_data = await state.get_data()
    courier_phone_number = message.contact.phone_number
    order_id = courier_data['order_id']

    await state.clear()

    await orm_add_courier(session=session,
                          user_id = message.from_user.id,
                          username = message.from_user.username)
    await orm_update_courier(session=session,
                             user_id=message.from_user.id,
                             order_id=order_id,
                             phone_number=courier_phone_number)

    await orm_update_customer_info(session=session,
                                   search_by="order_id",
                                   search_value=order_id,
                                   in_execution=True,
                                   courier_id = message.from_user.id)

    user_data = await orm_get_order(session=session, order_id=order_id)
    user_username = user_data.username
    user_phone = user_data.order_phone_number
    user_id = user_data.user_id

    await message.bot.send_message(text = user_text["the_order_was_taken"].format(order_id=order_id,
                                                                                  username=message.from_user.username,
                                                                                  phone_number=courier_phone_number),
                                   chat_id=user_id)
    await message.answer(text = courier_text["the_order_was_taken"].format(order_id=order_id,
                                                                                username=user_username,
                                                                                phone_number=user_phone),
                         reply_markup = await to_main_menu_kbds())

