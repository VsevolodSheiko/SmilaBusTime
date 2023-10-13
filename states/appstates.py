from aiogram.fsm.state import State, StatesGroup

class MyStates(StatesGroup):
    admin = State()
    waiting_for_message = State()
    ask_for_photo = State()
    waiting_for_photo = State()
    sending_the_message = State()
    
    get_buses_default = State()
    get_full_buses = State()