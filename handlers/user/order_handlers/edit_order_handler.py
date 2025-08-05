from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from common.filters.order_in_execution_filter import OrderInExecutionFilter
from database.sessions.user_session.order_session import (orm_get_customer_info,
                                                          orm_update_customer_info, orm_delete_order)
from common.texts.user_texts import user_text
from common.states import EditOrder, CreateOrder
from kbds.reply_kbds.user_reply_kbds import (edit_order_kbds,
                                             skip_kbds)
from kbds.inline_kbds.user_inline_kbds import (my_order_btns,
                                               to_main_menu_kbds)

edit_order_router = Router()

@edit_order_router.message(OrderInExecutionFilter())
async def f_order_in_execution(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    try:
        await message.edit_reply_markup(reply_markup=None)
    except:
        pass
    await message.answer(text=user_text['order_in_execution_error'],
                         reply_markup= await to_main_menu_kbds())

@edit_order_router.callback_query(F.data == 'edit_order')
async def f_edit_order(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await orm_update_customer_info(session=session,
                                   search_value=callback.from_user.id,
                                   in_edit=True)

    await state.set_state(EditOrder.edit_order_btn)

    try:
        await callback.message.edit_text(text=user_text['edit_order'],
                                         reply_markup=await edit_order_kbds())
    except:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(text=user_text['edit_order'],
                                      reply_markup=await edit_order_kbds())

@edit_order_router.message(EditOrder.edit_order_btn, F.text == 'Фото 📸')
async def f_edit_order_photo(message: Message, state: FSMContext):
    await state.set_state(EditOrder.edit_order_photo)
    await message.answer(text=user_text['order_photo'],
                         reply_markup = await skip_kbds())

@edit_order_router.message(EditOrder.edit_order_photo, F.photo)
async def f_editing_order_photo(message: Message, state: FSMContext, session: AsyncSession):
    if message.media_group_id:
        return
    await state.clear()
    data = await orm_get_customer_info(session, message.from_user.id)

    main_order_text = user_text['my_order'].format(
        order_id=data.order_id,
        description=data.order_text,
        phone_number=data.order_phone_number,
        username=data.username)
    await orm_update_customer_info(session = session,
                                   search_value=message.from_user.id,
                                   order_photo=message.photo[-1].file_id,
                                   in_edit=False)

    await message.answer_photo(caption=user_text['edit_order_applied'].format(value='фото') + main_order_text,
                                photo=message.photo[-1].file_id,
                               reply_markup=await my_order_btns())

@edit_order_router.message(EditOrder.edit_order_photo, F.text == 'Пропустить')
async def f_editing_order_photo_skip(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    data = await orm_get_customer_info(session, message.from_user.id)

    main_order_text = user_text['my_order'].format(
        order_id=data.order_id,
        description=data.order_text,
        phone_number=data.order_phone_number,
        username=data.username)

    await orm_update_customer_info(session=session,
                                   search_value=message.from_user.id,
                                   order_photo=None,
                                   in_edit=False)
    await message.answer(text=user_text['edit_order_applied'].format(value='фото') + main_order_text,
                         reply_markup=await my_order_btns())

@edit_order_router.message(EditOrder.edit_order_btn, F.text == 'Описание 🗒️')
async def f_edit_order_description(message: Message, state: FSMContext):
    await state.set_state(EditOrder.edit_order_description)
    await message.answer(text=user_text['order_text'],
                         reply_markup=await skip_kbds())

@edit_order_router.message(EditOrder.edit_order_description, F.text == 'Пропустить')
async def f_edit_order_text_skip(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    data = await orm_get_customer_info(session, message.from_user.id)
    await orm_update_customer_info(session=session,
                             search_value=message.from_user.id,
                             in_edit=False)
    main_order_text = user_text['edit_order_applied'].format(value='описание') + user_text['my_order'].format(
        order_id=data.order_id,
        description=data.order_text,
        phone_number=data.order_phone_number,
        username=data.username)

    if data.order_photo:
        await message.answer_photo(caption=main_order_text,
                                   reply_markup=await my_order_btns(),
                                   photo=data.order_photo)
        return
    await message.answer(text=main_order_text,
                         reply_markup=await my_order_btns())

@edit_order_router.message(EditOrder.edit_order_description, F.text)
async def f_edit_order_text(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    data = await orm_get_customer_info(session, message.from_user.id)

    main_order_text = user_text['edit_order_applied'].format(value='описание') + user_text['my_order'].format(
        order_id=data.order_id,
        description=message.text,
        phone_number=data.order_phone_number,
        username=data.username)

    await orm_update_customer_info(session=session,
                                   search_value=message.from_user.id,
                                   order_text=message.text,
                                   in_edit=False)
    if data.order_photo:
        await message.answer_photo(caption=main_order_text,
                                   reply_markup=await my_order_btns(),
                                   photo=data.order_photo)
        return
    await message.answer(text=main_order_text,
                         reply_markup=await my_order_btns())

@edit_order_router.message(EditOrder.edit_order_btn, F.text == 'Удалить и заполнить заново 🔄')
async def f_edit_order_full(message: Message, state: FSMContext, session: AsyncSession):
    await orm_delete_order(session, message.from_user.id)

    await state.set_state(CreateOrder.order_text)
    await message.answer(text=user_text['order_text'])

