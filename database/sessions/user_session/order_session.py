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
                           order_id: int,
                           order_text: str,
                           order_photo: str,
                           order_phone_number: str) -> Customer:
    customer = Customer(user_id=user_id,
                        username=username,
                        order_id=order_id,
                        order_text=order_text,
                        order_photo=order_photo,
                        order_phone_number=order_phone_number)
    session.add(customer)
    await session.commit()

async def orm_get_costumer_attr(session: AsyncSession,
                                attr: str):
    column_data = getattr(Customer, attr)
    result = await session.execute(select(column_data))
    return result.scalars().all()