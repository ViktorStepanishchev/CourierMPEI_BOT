from aiogram.types import CallbackQuery, Message
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import base
from base import ff, order_base

import keyboard, text
import back
from states import all_state

router = Router()

@router.message(Command("start")) # Стартовое окно
async def start(message:Message):
    await message.answer(text.start_text, reply_markup=keyboard.main_keyboard)
@router.callback_query(F.data == 'order') # Кнопка создать заказ
async def order(clbck: CallbackQuery, state: FSMContext):
    ff.execute(f"SELECT id FROM orders WHERE id = ?", (clbck.from_user.id,))
    if ff.fetchone() is None:
        await state.set_state(all_state.wait_message_order)
        await clbck.message.edit_text(text.order_text, reply_markup=keyboard.back_keyboard)
    else:
        await clbck.message.edit_text(text.order_is_get_text, reply_markup=keyboard.del_keyboard)

@router.message(all_state.wait_message_order) # Действия после написания заказа пользователем
async def get_order(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer(text.error_order_None_text, reply_markup=keyboard.back_keyboard)
    else:
        await state.update_data(wait_message_order = message.text)
        ff.execute(f"SELECT id FROM orders WHERE id = ?", (message.from_user.id,))
        num_now_order = back.prov(back.all_id_orders)
        ff.execute(f"INSERT INTO orders VALUES (?, ?, ?, ?, ?)", (back.last_string_bd()[0] + 1, num_now_order, message.text, message.from_user.id, "СВОБОДЕН"))
        order_base.commit()
        keyboard.add_inline_order_for_courier()
        await message.chat.delete_message(message_id=message.message_id - 1)
        await message.chat.delete_message(message_id=message.message_id - 2)
        await message.answer(f"Ваш заказ #{num_now_order}"+text.get_order_text, reply_markup=keyboard.back_keyboard)
        base.output_base()
        await state.clear()

@router.callback_query(F.data == 'courier') #Кнопка посмотреть заказы пользователей (стать курьером)
async def courier(clbck: CallbackQuery):
    await clbck.message.edit_text(text.courier_text, reply_markup=keyboard.order_keyboard)

@router.callback_query(F.data == 'help') #Кнопка помощи
async def help(clbck: CallbackQuery):
    await clbck.message.edit_text(text.help_text, reply_markup=keyboard.help_keyboard)

@router.callback_query(F.data == 'back') #Кнопка вернуться назад
async def back_button(clbck: CallbackQuery):
    await clbck.message.edit_text(text.start_text, reply_markup=keyboard.main_keyboard)

@router.callback_query(F.data == "my_order") #Кнопка просмотра собственного заказа
async def my_order(clbck: CallbackQuery):
    ff.execute(f"SELECT orderr FROM orders WHERE id = (?)", (clbck.from_user.id,))
    if ff.fetchone() is None:
        await clbck.message.edit_text("Здесь пока что пусто 😶", reply_markup=keyboard.back_keyboard)
    else:
        num_of_order = ff.execute(f"SELECT num FROM orders WHERE id = (?)", (clbck.from_user.id,)).fetchone()[0]
        descript_of_order = ff.execute(f"SELECT orderr FROM orders WHERE id = (?)", (clbck.from_user.id,)).fetchone()[0]
        await clbck.message.edit_text(f"""

        Ваш заказ #{num_of_order}

        ===ОПИСАНИЕ===

        {descript_of_order}

        ==============

        """, reply_markup=keyboard.del_keyboard)

@router.callback_query(F.data == 'delete_order') #Кнопка удаления своего заказа
async def delete_order(clbck: CallbackQuery):
    keyboard.delete_inline_order_for_courier((ff.execute(f"SELECT num_iterat FROM orders WHERE id = (?)", (clbck.from_user.id,))).fetchone()[0])
    ff.execute(f"DELETE FROM orders WHERE id = (?)", (clbck.from_user.id,))
    order_base.commit()
    base.output_base()
    await clbck.message.edit_text(text.delete_order_text, reply_markup=keyboard.after_del_keyboard)

@router.callback_query(F.data == 'get_order_clbck') #Кнопка взятия заказа
async def get_current_order(clbck: CallbackQuery):
    ff.execute(f"UPDATE orders SET state_orderr = (?) WHERE id = (?)", ("ЗАНЯТ", clbck.from_user.id))
    order_base.commit()
    base.output_base()
    await clbck.message.edit_text("Вы типо взяли заказ (я ещё в бета-тесте, поэтому я пока не выполняю основных функций)", reply_markup=keyboard.back_keyboard)
@router.callback_query(F.data.startswith("")) #Кнопка просмотра определенного заказа (курьер)
async def all_orders(clbck: CallbackQuery):
    order_descrip = list(ff.execute(f"SELECT orderr FROM orders WHERE num = (?)", (clbck.data,)).fetchone())[0]
    await clbck.message.edit_text(f"""
    
Заказ #{clbck.data}

===ОПИСАНИЕ===

{order_descrip}

==============

""", reply_markup=keyboard.get_order_keyboard)

@router.message() #Обработка любого текста
async def start(message:Message):
    await message.answer(text.start_text, reply_markup=keyboard.main_keyboard)