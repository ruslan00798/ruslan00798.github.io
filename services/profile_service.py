# ==========================
# profile_service.py
#
# Данные пользователя
# ==========================


from database.requests import get_xp

async def get_user_xp(user_id: int):
    """
    Возвращает XP пользователя.
    """

    return await get_xp(user_id)