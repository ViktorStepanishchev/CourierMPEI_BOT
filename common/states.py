from aiogram.fsm.state import State, StatesGroup

class CreateOrder(StatesGroup):
    order_text = State()
    order_photo = State()
    order_phone_number = State()