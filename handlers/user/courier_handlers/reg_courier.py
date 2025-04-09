from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from common.texts.user_texts import courier_text
from kbds.inline_kbds.user_inline_kbds import orders_kbds

view_orders_router = Router()

@view_orders_router.callback_query(F.data.startswith('courier_'))
async def f_reg_courier(callback: CallbackQuery, session: AsyncSession):
    callback_data = callback.data.split("_")
    if callback_data == 'courier': page=0
    else: page = int(callback.data.split("_")[-1])

    await callback.message.edit_text(text=courier_text['view_orders'],
                                     reply_markup = await orders_kbds(session, page))
