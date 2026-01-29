from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from logic.users.register import register_user
from api.api_client import *
from aiogram import Router
from keyboards.inline.keys import rename_twitch_keyboard
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user : UserResponse = await get_user(message.from_user.id)
    if (user):
        
        await message.answer(
            f"Привет, <b>{user.twitch_nickname}</b>. Ты уже зарегистрировался, желаешь поменять никнейм?",
            reply_markup=await rename_twitch_keyboard()
        )

    else:
        await register_user(message, state)

    await message.delete()