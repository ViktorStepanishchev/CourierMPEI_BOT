from aiogram.filters import Filter
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.sessions.user_session.order_session import orm_get_order

class OrderInEditOrDeletedFilter(Filter):
    async def __call__(self, callback: CallbackQuery, session: AsyncSession):
        callback_data = callback.data.split("_")
        order_id = callback_data[-2]
        if len(callback_data) > 2 and callback.message.chat.type in ['private']:
            order_data = await orm_get_order(session=session, order_id=order_id)
            return order_data is None or order_data.in_edit