import aiohttp
from config import FASTAPI_URL
from muhanjanbattle_models.user import UserResponse, UserCreate, UserUpdate
from typing import Optional


TIMEOUT = aiohttp.ClientTimeout(total=10)

async def get_user(telegram_id: int) -> UserResponse | None:
    url = f"{FASTAPI_URL}/users/{telegram_id}"  

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return UserResponse(**data)
            if response.status == 404:
                return None
            else:
                error_text = await response.text()
                raise Exception(f"Backend API error: {response.status} — {error_text}")


async def post_user(user: UserCreate) -> Optional[UserResponse]:
    url = f"{FASTAPI_URL}/users"
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        async with session.post(
            url,
            json=user.model_dump(),
            headers={"Content-Type": "application/json"}
        ) as response:
            if response.status == 200:
                data = await response.json()
                return UserResponse(**data)
            elif response.status == 400:
                return None
            else:
                error_text = await response.text()
                print(f"❗ Серверная ошибка: {response.status} — {error_text}")
                return None



async def patch_user(telegram_id: int, user: UserUpdate) -> Optional[UserResponse]:
    url = f"{FASTAPI_URL}/users/{telegram_id}"
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        async with session.patch(
            url,
            json=user.model_dump(exclude_unset=True),
            headers={"Content-Type": "application/json"}
        ) as response:
            if response.status == 200:
                data = await response.json()
                return UserResponse(**data)
            elif response.status == 400:
                print(f"⚠️ Ошибка валидации: {await response.text()}")
                return None
            elif response.status == 404:
                print(f"⚠️ Пользователь с telegram_id={telegram_id} не найден")
                return None
            else:
                error_text = await response.text()
                print(f"❗ Серверная ошибка: {response.status} — {error_text}")
                return None