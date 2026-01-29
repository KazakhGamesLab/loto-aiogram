from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
#from logic.users.register import register_user
from api.api_client import *
from aiogram import Router
from keyboards.inline.keys import get_webapp_keyboard
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"🎉 <b>Добро пожаловать в ЛОТО с Муханджаном!</b>\n\n"
        f"🎰 <i>Сыграй в лото прямо во время стрима!</i>\n\n"
        f"✨ Как это работает:\n"
        f"• Получи уникальную карту лото после регистрации\n"
        f"• Следи за стримом Муханджана на Twitch\n"
        f"• Зачёркивай выпавшие числа в боте в реальном времени\n"
        f"🎁 Призы: донаты, подписки, мерч и сюрпризы от Муханджана!\n\n",
        reply_markup=await get_webapp_keyboard()
    )

    await message.delete()