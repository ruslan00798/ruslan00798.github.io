# ==========================
# dictionary_service.py
#
# Отвечает за работу со словарём
# ==========================

from database.requests import  get_word, create_word


async def find_word(word: str):
    """
    Ищет слово в словаре.
    """

    return await get_word(word)



async def get_or_create_word(word: str, translation: str,) -> int:
    """
    Возвращает id слова.
    Если слова нет - создаёт его.
    """

    row = await find_word(word)

    if row:
        return row["id"]
    
    return await create_word(
        word,
        translation,
        language="en",
        category="history",
        level="1"
    )
     
