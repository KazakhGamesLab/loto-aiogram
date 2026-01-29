import re

async def is_valid_twitch_nickname(nickname: str) -> bool:
    if not isinstance(nickname, str):
        return False

    nickname = nickname.strip()

    if not nickname:
        return False

    if len(nickname) > 25:
        return False

    if not re.fullmatch(r"^[a-zA-Z0-9_]+$", nickname):
        return False

    reserved = {
        "admin", "moderator", "mod", "streamer", "twitch", "bot",
        "support", "customer_support", "staff", "test", "null", "/start", "/rename_twitch"
    }
    if nickname.lower() in reserved:
        return False

    return True