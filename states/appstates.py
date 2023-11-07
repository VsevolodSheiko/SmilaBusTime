from aiogram.fsm.state import State, StatesGroup

class MyStates(StatesGroup):
    admin = State()
    waiting_for_message = State()
    ask_for_photo = State()
    waiting_for_photo = State()
    sending_the_message = State()

    update_route_get_buses = State()
    update_route_choose_column = State()
    update_route_choose_field = State()
    update_route_new_data = State()

    
    get_buses_default = State()
    get_full_buses = State()