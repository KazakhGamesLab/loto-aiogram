from aiogram.fsm.state import State, StatesGroup

class UserRegistration(StatesGroup):
    waiting_for_twitch_nickname = State()
    waiting_for_rename_twitch_nickname = State()
