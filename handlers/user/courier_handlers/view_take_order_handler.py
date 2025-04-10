from Demos.win32ts_logoff_disconnected import session
from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from common.texts.user_texts import courier_text
from common.filters.order_in_edit_or_deleted_filter import OrderInEditOrDeletedFilter
from kbds.inline_kbds.user_inline_kbds import orders_kbds
from kbds.inline_kbds.user_inline_kbds import take_order_kbds
from database.sessions.user_session.order_session import orm_get_order

view_take_order_router = Router()

@view_take_order_router.callback_query(F.data.startswith('courier_'))
async def f_view_orders(callback: CallbackQuery, session: AsyncSession):
    callback_data = callback.data.split("_")[-1]
    if callback_data == 'courier': page=0
    else: page = int(callback_data)

    try:
        await callback.message.edit_text(text=courier_text['view_orders'],
                                         reply_markup = await orders_kbds(session, page))
    except:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(text=courier_text['view_orders'],
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