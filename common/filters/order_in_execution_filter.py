from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union

from database.sessions.user_session.order_session import orm_get_customer_info

class OrderInExecutionFilter(Filter):
    async def __call__(self, update: Union[CallbackQuery, Message], state: FSMContext, session: AsyncSession):
        user_data = await orm_get_customer_info(session=session,
                                           user_id=update.from_user.id)
        return user_data.in_execution is True