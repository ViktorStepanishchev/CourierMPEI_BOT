from aiogram.fsm.state import State, StatesGroup

class CreateOrder(StatesGroup):
    order_user_id = State()
    order_username = State()
    order_text = State()
    order_photo = State()
    order_phone_number = State()
    order_id = State()