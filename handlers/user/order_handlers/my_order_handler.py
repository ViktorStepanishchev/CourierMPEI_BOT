import asyncio
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession

from common.texts.user_texts import user_text
from database.sessions.user_session.order_session import (orm_get_customer_info,
                                                          orm_delete_order)
from kbds.inline_kbds.user_inline_kbds import (my_order_empty_btns,
                                               my_order_btns,
                                               delete_order_kbds,
                                               main_kbds)

my_order_router = Router()

@my_order_router.callback_query(F.data == 'my_order')
async def f_my_order_handler(callback: CallbackQuery, session: AsyncSession):
    data = await orm_get_customer_info(session=session,
                                 user_id=callback.from_user.id)

    if data is None:
        await callback.message.edit_text(text = user_text['order_is_empty'],
                                         reply_markup=await my_order_empty_btns())
        return

    if data.order_photo is None:
        await callback.message.edit_text(text = user_text['my_order'].format(order_id=data.order_id,
                                                                             description=data.order_text,
                                                                             phone_number=data.order_phone_number,
                                                                             username=data.username),
                                         reply_markup=await my_order_btns())
        return

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer_photo(photo=data.order_photo,
                                        caption=user_text['my_order'].format(order_id = data.order_id,
                                                                             description=data.order_text,
                                                                             phone_number=data.order_phone_number,
                                                                             username=data.username),
                                        reply_markup=await my_order_btns())

@my_order_router.callback_query(F.data == 'delete_order')
async def f_delete_order(callback: CallbackQuery, session: AsyncSession):
    try:
        await callback.message.edit_text(text = user_text['first_delete_order'],
                                  reply_markup=await delete_order_kbds())
    except:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(text = user_text['first_delete_order'],
                                      reply_markup=await delete_order_kbds())

@my_order_router.callback_query(F.data == 'approve_delete_order')
async def f_approve_delete_order(callback: CallbackQuery, session: AsyncSession):
    await orm_delete_order(session=session,
                           user_id = callback.from_user.id)
    await callback.message.edit_text(text = user_text['order_is_deleted'])
    await asyncio.sleep(0.8)
    await callback.message.answer(text = user_text['start'],
                                  reply_markup=await main_kbds())

