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
                           order_phone_number: str) -> None:
    customer = Customer(user_id=user_id,
                        username=username,
                        order_id=order_id,
                        order_text=order_text,
                        order_photo=order_photo,
                        order_phone_number=order_phone_number)
    session.add(customer)
    await session.commit()

async def orm_get_costumer_attr(session: AsyncSession,
                                attr: str) -> Customer:
    result = await session.execute(select(getattr(Customer, attr)))
    return result.scalars().all()

async def orm_get_free_orders(session: AsyncSession):
    result = await session.execute(select(Customer.order_id).where(Customer.in_execution == False))
    return result.scalars().all()

async def orm_update_customer_info(session: AsyncSession,
                                   search_by: str = "user_id",
                                   search_value: str = None,
                                   **kwargs) -> None:
    fields = ['order_text', 'order_photo', 'in_execution', 'in_edit', 'courier_id']
    result = await session.execute(select(Customer).where(getattr(Customer, search_by) == search_value))
    user_data = result.scalar_one_or_none()
    for field in fields:
        if field in kwargs and kwargs[field] != getattr(user_data, field):
            setattr(user_data, field, kwargs[field])
            await session.commit()

async def orm_delete_order(session: AsyncSession,
                           user_id: int) -> None:
    await session.execute(delete(Customer).where(Customer.user_id == user_id))
    await session.commit()

async def orm_get_order(session: AsyncSession,
                        order_id: int) -> Customer:
    result = await session.execute(select(Customer).where(Customer.order_id == order_id))
    return result.scalars().first()

async def orm_toggle_order_in_edit(session: AsyncSession,
                                   user_id: int) -> None:
    result = await session.execute(select(Customer).where(Customer.user_id == user_id))
    customer_data = result.scalars().first()
    if customer_data is not None and customer_data.in_edit:
        customer_data.in_edit = not customer_data.in_edit
        await session.commit()
