import asyncio
from aiogram import Bot
import json
from redis import asyncio as aioredis
from config import REDIS_URL
import logging

logger = logging.getLogger(__name__)


async def start_redis_listener(bot):
    redis = aioredis.from_url(REDIS_URL)
    logger.info("Redis listener запущен и ожидает сообщения...")

    try:
        while True:
            result = await redis.blpop("telegram:responses", timeout=0)
            if not result:
                continue  

            key, data = result
            if isinstance(data, bytes):
                data = data.decode('utf-8')

            try:
                resp = json.loads(data)
                await bot.send_message(resp["user_id"], resp["text"])
                logger.debug(f"Отправлено сообщение пользователю {resp['user_id']}")
            except Exception as e:
                logger.error(f"Не удалось обработать сообщение: {data}, ошибка: {e}")

    except asyncio.CancelledError:
        logger.info("Redis listener остановлен по запросу.")
        raise  
    except Exception as e:
        logger.critical(f"Критическая ошибка в listener: {e}")
        raise
    finally:
        await redis.close()