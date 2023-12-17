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
num_of_order_in_mass = 0

@router.message(Command("start"))
async def start(message:Message):
    await message.answer(text.start_text, reply_markup=keyboard.main_keyboard)

@router.callback_query(F.data == 'order')
async def order(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(all_state.wait_message_order)
    await clbck.message.edit_text(text.order_text, reply_markup=keyboard.back_keyboard)

@router.message(all_state.wait_message_order)
async def get_order(message: Message, state: FSMContext):
    await state.update_data(wait_message_order = message.text)
    ff.execute(f"SELECT id FROM orders WHERE id = ?;", (message.from_user.id,))
    # if ff.fetchone() is None:
    ff.execute(f"INSERT INTO orders VALUES (?, ?, ?)", (back.prov(back.all_id_orders), message.text, message.from_user.id))
    order_base.commit()
    keyboard.ale()
    base.output_base()
    await message.answer(text.get_order_text, reply_markup=keyboard.back_keyboard)
    # else:
    #     await message.answer(text.order_is_get, reply_markup=keyboard.back_keyboard)
    await state.clear()

@router.callback_query(F.data == 'courier')
async def courier(clbck: CallbackQuery):
    await clbck.message.edit_text(text.courier_text, reply_markup=keyboard.order_keyboard.as_markup())

@router.callback_query(F.data == 'help')
async def help(clbck: CallbackQuery):
    await clbck.message.edit_text(text.help_text, reply_markup=keyboard.help_keyboard)

@router.callback_query(F.data == 'back')
async def help(clbck: CallbackQuery):
    await clbck.message.edit_text(text.start_text, reply_markup=keyboard.main_keyboard)

@router.message()
async def start(message:Message):
    await message.answer(text.start_text, reply_markup=keyboard.main_keyboard)