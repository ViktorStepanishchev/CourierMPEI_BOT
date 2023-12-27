from aiogram.fsm.state import State, StatesGroup

class all_state(StatesGroup):
    wait_message_order = State()
