from states.states import UserRegistration
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from messages import PLEASE_INPUT_TWITCH, PLEASE_INPUT_NEW_TWITCH


async def register_user(message: Message, state: FSMContext) -> None:
    await message.answer(PLEASE_INPUT_TWITCH)
    await state.set_state(UserRegistration.waiting_for_twitch_nickname)
    await message.delete()


async def rename_user_twitch(message: Message, state: FSMContext) -> None:
    await message.answer(PLEASE_INPUT_NEW_TWITCH)
    await state.set_state(UserRegistration.waiting_for_rename_twitch_nickname)
    await message.delete()


