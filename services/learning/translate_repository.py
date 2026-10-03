from database.requests import (
    get_history_by_id,
    get_language,
    get_word,
    save_history,
)

class TranslateRepository:
    async def get_history_by_id(self, user_id: int, history_id: int,):
        return await get_history_by_id(user_id,  history_id)

    async def get_language(self, user_id: int):
        return await get_language(user_id)

    async def get_word(self, text: str, language: str):
        return await get_word(text, language)

    async def save_history(
        self,
        user_id: int,
        text: str,
        translated: str 
    ):

        return await save_history(
            user_id,
            text,
            translated
        )