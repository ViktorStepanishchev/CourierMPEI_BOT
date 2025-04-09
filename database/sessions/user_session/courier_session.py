from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Courier

async def orm_add_courier(session: AsyncSession,
                               user_id: int,
                               username: str) -> None:
    session.add(Courier(
        user_id=user_id,
        username=username))
    await session.commit()

async def orm_update_courier(session: AsyncSession,
                             user_id: int,
                             **kwargs):
    result = await session.execute(select(Courier).where(Courier.user_id == user_id))
    user_data = result.scalar_one_or_none()

    fields = ['user_id', 'username', 'order_id']
    for field in fields:
        if field in kwargs and kwargs[field]:
            setattr(user_data, field, kwargs[field])
            await session.commit()