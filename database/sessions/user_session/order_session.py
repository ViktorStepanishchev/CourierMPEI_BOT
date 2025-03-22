from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Customer

async def orm_get_customer_info(session: AsyncSession,
                                user_id: int) -> Customer:
    data = await session.execute(select(Customer).where(Customer.user_id == user_id))
    return data.scalars().first()

async def orm_add_customer(session: AsyncSession,
                           user_id: int,
                           username: str,
                           order_id: int) -> Customer:
    customer = Customer(id=id,
                        user_id=user_id,
                        username=username,
                        order_id=order_id)
    session.add(customer)
    await session.commit()