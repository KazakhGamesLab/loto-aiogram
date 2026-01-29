from aiogram.fsm.context import FSMContext
from states.states import UserRegistration
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from api.api_client import post_user, patch_user
from aiogram import Router, F
from logic.users.register import rename_user_twitch
from messages import REGISTER_FINALLY, TWITCH_NICKNAME_ALREADY, TWITCH_RENAME_SUCCESS, TWITCH_NICKNAME_NOT_VALID
from logic.users.validator import is_valid_twitch_nickname
from muhanjanbattle_models.user import UserCreate, UserUpdate

router = Router()

@router.message(UserRegistration.waiting_for_twitch_nickname)
async def handle_twitch_nick(message: Message, state: FSMContext) -> None:

    if (not await is_valid_twitch_nickname(message.text.strip())):
        await message.answer(TWITCH_NICKNAME_NOT_VALID)
        return

    user_data = UserCreate(
        telegram_id=message.from_user.id,
        twitch_nickname=message.text.strip(),
        first_name=message.from_user.first_name,
        telegram_username=message.from_user.username or 'Неизвестный'
    )

    result = await post_user(user_data)

    if result is not None:
        await message.answer(REGISTER_FINALLY)
        await state.clear()
    else:
        await message.answer(TWITCH_NICKNAME_ALREADY)

    await message.delete()


@router.message(UserRegistration.waiting_for_rename_twitch_nickname)
async def handle_twitch_nick(message: Message, state: FSMContext) -> None:

    if (not await is_valid_twitch_nickname(message.text.strip())):
        await message.answer(TWITCH_NICKNAME_NOT_VALID)
        return

    update_data = UserUpdate(twitch_nickname=message.text.strip(), telegram_username=message.from_user.username)
    result = await patch_user(telegram_id=message.from_user.id, user=update_data)

    if result is not None:
        await message.answer(TWITCH_RENAME_SUCCESS + f'{result.twitch_nickname}')
        await state.clear()
    else:
        await message.answer(TWITCH_NICKNAME_ALREADY)

    await message.delete()


@router.callback_query(F.data == "rename_twitch")
async def rename_twitch_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await rename_user_twitch(callback.message,  state)
    await callback.message.delete()

@router.message(Command("rename_twitch"))
async def rename_twitch_command(message: Message, state: FSMContext) -> None:
    await rename_user_twitch(message,  state)
    await message.delete()

    