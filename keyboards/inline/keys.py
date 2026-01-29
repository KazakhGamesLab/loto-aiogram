from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import WEB_APP_URL

async def get_webapp_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text="Играть",
        web_app=WebAppInfo(url=WEB_APP_URL)
    ))
    return keyboard.as_markup()