# dictionary_service.py
import logging

logger = logging.getLogger(__name__)

class DictionaryService:
    def __init__(self, repository,  history_service):
        self.repository = repository
        self.history_service = history_service
        
    async def find_word(self, word: str, language: str):
        """
        Ищет слово в словаре.
        """
        logger.debug(
            "поиск слова в словаре: word=%s language=%s",
            word,
            language
        )

        return await self.repository.get_word(word, language)



    async def get_or_create_word(self, word: str, translation: str, language: str) -> int:
        """
        Возвращает id слова.
        Если слова нет - создаёт его.
        """

        row = await self.find_word(word, language)

        if row:
            logger.debug(
                "Слово найдено в словаре: word=%s language=%s word_id=%s",
                word,
                language,
                row["id"],
            )

            return row["id"]
        
        word_id = await self.repository.create_word(
            word,
            translation,
            language=language,
            category="history",
            level = "1"
        )

        logger.info(
            "Создано новое слово в словаре: word=%s language=%s word_id=%s", 
            word, 
            language, 
            word_id,
        )
        return word_id
        
    # =====================
    # Добавляем слово из истории переводов
    # =====================

    async def add_word_from_history(self, user_id: int, history_id: int,):

        logger.info(
            "добавление слова из истории: user_id=%s history_id=%s",
            user_id,
            history_id,
        )

        try:

            history = await self.history_service.get_translation_history (user_id, history_id)

            if history is None:
                logger.warning(
                    "История переводов не найдена: user_id=%s history_id=%s",
                    user_id,
                    history_id,
                )
                return {
                    "success": False,
                    "error": "history_not_found"
                }

            language = await self.repository.get_language(user_id) 
            
            word_id = await self.get_or_create_word(
                history["original_text"],
                history["translated_text"],
                language
            )


            await self.repository.add_word_progress(user_id, word_id)

            logger.info(
                "Слово добавлено пользователю из истории: user_id=%s history_id=%s word_id=%s",
                user_id,
                history_id,
                word_id,
            )

            return {
                "success": True,
                "word": history["original_text"],
                "translation": history["translated_text"]
                
            }

        except Exception:
            logger.exception( 
                "Ошибка при добавлении слова из истории: " "user_id=%s history_id=%s", 
                user_id, 
                history_id, 
            ) 
            raise



            