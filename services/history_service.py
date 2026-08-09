# ==========================
# history_service.py
#
# Работа с историей переводов
# ==========================


from database.requests import get_history_by_id

async def get_translation_history(user_id: int, history_id: int):

    """
    Получает перевод пользователя из истории.
    """

    return await get_history_by_id(user_id, history_id)