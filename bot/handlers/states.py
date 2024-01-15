from aiogram.fsm.state import State, StatesGroup


class Settings(StatesGroup):
    keywords = State()
    mode = State()
    pages_count = State()
