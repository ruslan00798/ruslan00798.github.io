#translation_service.py
import logging

from services.translator import (
    add_harakat_simple,
    translate,
)

from models.translation import (
    TranslationError,
    TranslationResult,
    TranslationHistory,
    AudioResult
)

from services.tts import generate_audio



logger = logging.getLogger(__name__)


# ==========================================
# Перевод текста
# ==========================================
class TranslateService:
    def __init__(self, repository):
        self.repository = repository
        
    async def process_translation(
        self,    
        user_id: int,
        text: str,
    ) -> TranslationResult:

        logger.info(
            "Начало перевода: user_id=%s",
            user_id,
        )

        text = text.strip()

        if not text:
            logger.warning(
                "пустой текст для перевода: user_id=%s",
                user_id,
            )
            return TranslationResult (
                error = TranslationError.EMPTY_TEXT,
            )

        # Получаем выбранный язык пользователя
        language = await self.repository.get_language(user_id)

        if not language:
            logger.warning(
                "язык не выбран: user_id=%s",
                user_id,
            )
            return TranslationResult(
                error = TranslationError.LANGUAGE_NOT_SELECTED,
            )

        logger.info(
            "Translation request: user=%s language=%s",
            user_id,
            language,
            
        )

        # ======================================
        # Сначала ищем готовое слово в БД
        # ======================================

        db_word = await self.repository.get_word(text, language,)

        if db_word:
            logger.info(
                "перевод найден в БД: user_id=%s, language=%s",
                user_id,
                language,
            )

            translated = db_word["translation"]

        else:
            logger.info(
                "перевод не найден в БД, обращаемся к переводчику: user_id=%s, language=%s",
                user_id,
                language,
            )

            translated = await translate(text, language)

            if not translated:
                logger.error(
                    "Переводчик вернул пустой результат: user_id=%s, language=%s",
                    text,
                    translated,
                )
                return TranslationResult(
                    error = TranslationError.TRANSLATION_FAILED,
                )

            logger.info(
                "перевод успешно получен: user_id=%s, language=%s",
                user_id,
                language,
            )

        # ======================================
        # Арабский текст
        # ======================================

        if language == "ar":
            logger.info(
                "добавления харакатов: user_id=%s",
                user_id,
            )
            translated = add_harakat_simple(translated)
    
        history_id = await self.repository.save_history(
            user_id,
            text,
            translated,
        )

        logger.info(
            "Translation saved history_id=%s",
            history_id,
        )

        logger.info( 
            "Перевод успешно завершён: user_id=%s", 
            user_id, 
        )

        return TranslationResult(
        
            translated =  translated,
            history_id = history_id,
        )


    # ==========================================
    # Повторить перевод
    # ==========================================

    async def get_translation_for_repeat(
        self,    
        user_id: int,
        history_id: int,
    ) -> TranslationHistory | None:

        logger.info(
            "запрос повторного перевода: user_id=%s history_id=%s",
            user_id,
            history_id,
        )

        history =  await self.repository.get_history_by_id(
            user_id,
            history_id,
        )

        if not history:
            logger.warning(
                "История перевода не найдена: user_id=%s, history_id=%s",
                user_id,
                history_id,
            )
            return None

        logger.info(
            "История перевода найдена: user_id=%s history_id=%s",
            user_id,
            history_id,
        )
        return TranslationHistory(
            id=history["id"],
            translated_text=history["translated_text"],
        )



    # ==========================================
    # Получить аудио перевода из истории
    # ==========================================

    async def get_audio_for_history(self, user_id: int, history_id: int,) -> AudioResult | None:

        logger.info(
            "запрос аудио: user_id=%s history_id=%s",
            user_id,
            history_id,
        )

        history = await self.repository.get_history_by_id(
            user_id,
            history_id,
        )

        if not history:
            logger.warning(
                "история для аудио не найдена: user=%s history_id=%s",
                user_id,
                history_id,
            )
            return None

        text = history["translated_text"]

        language = await self.repository.get_language(user_id)

        if not language:

            logger.error(
                "язык не найден: user=%s",
                user_id,
            )

            return None

        logger.info(
            "начало генерации аудио: user_id=%s, history_id=%s, language=%s",
            user_id,
            history_id,
            language,
        )  

        file_path = await generate_audio(
            text,
            language,
        )

        if not file_path:

            logger.error(
                "не удалось сгенерировать audio: user_id=%s, history_id=%s",
                user_id,
                history_id,
            )

            return None


        logger.info(
           "аудио успешно сгенерировано: user_id=%s, history_id=%s",
           user_id,
           history_id,
        )

        return AudioResult(
            file_path = file_path,
            text = text,
        )
