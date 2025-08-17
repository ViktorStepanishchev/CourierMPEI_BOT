from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from common.texts.user_texts import courier_text
from database.sessions.user_session.order_session import orm_get_free_orders

from kbds.inline_kbds.gen_inline_kbds import get_callback_btns

async def main_kbds():
    main_kbds = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сделать заказ! 🛒️", callback_data="order"),
         InlineKeyboardButton(text = "Стать курьером! 🏃🏼‍", callback_data="courier_0")],

        [InlineKeyboardButton(text="Мой заказ 📦", callback_data="my_order")],

        [InlineKeyboardButton(text = "Помощь ⚙", callback_data="help")]
    ])
    return main_kbds

async def order_is_done_kbds():
    btns = {
        "« Отмена": "back_to_main_menu",
        "Сформировать ✅": "order_done"
    }
    return await get_callback_btns(btns=btns)

async def my_order_btns():
    my_order = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Изменить 🔄', callback_data='edit_order'),
         InlineKeyboardButton(text='Удалить 🗑️', callback_data='delete_order')],
        [InlineKeyboardButton(text='« Вернуться', callback_data='back_to_main_menu')]
    ])
    return my_order

async def my_order_empty_btns():
    btns = {
        "Сделать заказ! 🛒️": "order",
        "« Вернуться": "back_to_main_menu"
    }
    return await get_callback_btns(btns=btns, sizes=(1,))

async def to_main_menu_kbds():
    btns = {
        "« Вернуться": "back_to_main_menu",
    }
    return await get_callback_btns(btns=btns)

async def delete_order_kbds():
    btns = {
        "Да" : "approve_delete_order",
        "Нет" : "back_to_main_menu"
    }
    return await get_callback_btns(btns=btns)

async def help_kbds():
    btns = {
        "« Вернуться" : "back_to_main_menu",
        "Вопрос админам ✉️" : "admin_call"
    }
    return await get_callback_btns(btns=btns)

async def orders_kbds(session: AsyncSession, page: int):

    orders_data_list = await orm_get_free_orders(session=session)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="back_to_main_menu"))
    for order_id in orders_data_list[page:page+5]:
        builder.button(text=courier_text['order_in_kbds'].format(order_id=order_id),
                       callback_data=f"order_{order_id}_{page}")
    builder.adjust(1)

    Nav_btns = []
    if page > 0:
        Nav_btns.append(InlineKeyboardButton(text="« Назад", callback_data=f"courier_{page - 5}"))

    if page + 5 < len(orders_data_list):
        Nav_btns.append(InlineKeyboardButton(text="Далее »", callback_data=f"courier_{page + 5}"))

    builder.row(*Nav_btns)

    return builder.as_markup()

async def take_order_kbds(order_id: int,
                     page: int):
    btns = {
        "Взять ✅": f"take_order_{order_id}_{page}",
        "« Назад": f"courier_{page}"
    }
    return await get_callback_btns(btns=btns, sizes=(1,))

async def back_to_orders_kbds(page: int):
    btns = {
        "« Назад": f"courier_{page}"
    }
    return await get_callback_btns(btns=btns, sizes=(1,))

