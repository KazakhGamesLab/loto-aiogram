from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

router = Router()

@router.error(ExceptionTypeFilter(TelegramBadRequest))
async def telegram_exception_handler(event: ErrorEvent) -> bool:
    if isinstance(event.exception, TelegramBadRequest):
        if "message to delete not found" in event.exception.message:
            return True  
    return False