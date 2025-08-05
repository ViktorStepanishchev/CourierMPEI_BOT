from aiogram.fsm.state import State, StatesGroup

class CreateOrder(StatesGroup):
    order_user_id = State()
    order_username = State()
    order_text = State()
    order_photo = State()
    order_phone_number = State()
    order_id = State()

class EditOrder(StatesGroup):
    edit_order_btn = State()
    edit_order_photo = State()
    edit_order_description = State()

class MessageToAdministration(StatesGroup):
    bot_msg_id = State()
    msg_id = State()
    username = State()

class AnswerMessageAdministration(StatesGroup):
    user_id = State()
    user_username = State()
    admin_msg_id = State()

class CourierStates(StatesGroup):
    order_id = State()
    waiting_for_phone = State()