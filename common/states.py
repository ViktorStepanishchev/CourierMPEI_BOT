from aiogram.fsm.state import State, StatesGroup

class CreateOrder(StatesGroup):
    order_user_id = State()
    order_username = State()
    order_text = State()
    order_photo = State()
    order_phone_number = State()
    order_id = State()

class MessageToAdministration(StatesGroup):
    msg_id = State()
    username = State()

class AnswerMessageAdministration(StatesGroup):
    user_id = State()
    user_username = State()
    admin_msg_id = State()