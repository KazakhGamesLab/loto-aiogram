import logging
import asyncio
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from create_bot import bot, dp
from config import WEBHOOK_URL
from rdis.redis_listener import start_redis_listener
from handlers import all_routers

async def set_commands():
    commands = [
        BotCommand(command='start', description='Старт'),
        BotCommand(command='rename_twitch', description='Поменять никнейм')
        ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def on_startup() -> None:
    await set_commands()
    await bot.set_webhook(WEBHOOK_URL)
    asyncio.create_task(start_redis_listener(bot))


async def on_shutdown() -> None:
    await bot.delete_webhook(drop_pending_updates=True)

def main() -> None:
    for router in all_routers:
        dp.include_router(router)

    dp.startup.register(on_startup)

    dp.shutdown.register(on_shutdown)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,  
        bot=bot 
    )
    webhook_requests_handler.register(app, path='/webhook')

    setup_application(app, dp, bot=bot)

    web.run_app(app, host='127.0.0.1', port=8000)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)  
    main() 
