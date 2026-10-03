from database.requests import  (
    add_word_progress, 
    get_word, 
    create_word, 
    get_language
)

class DictionaryRepository:
    async def add_word_progress(self, user_id: int, word_id: int):
        return await add_word_progress(user_id, word_id)

    async def get_word(self, word: str, language: str):
        return await get_word(word, language)

    async def create_word(
        self,
        word: str,
        translation: str,
        language: str,
        category: str,
        level: str  
    ):
        return await create_word(
            word,
            translation,
            language,
            category,
            level,
        )

    async def get_language(self, user_id: int):
        return await get_language(user_id)