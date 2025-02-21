from aiogram.fsm.state import StatesGroup, State


class ContactMe(StatesGroup):
    message = State()
