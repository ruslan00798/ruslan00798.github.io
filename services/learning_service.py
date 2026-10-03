import logging

from services.learning.result import LearningResult
from utils.xp import calculate_study_xp
from services.learning.constants import MODE_NEW, MODE_ERRORS, MODE_REVIEW
from services.learning.utils import check_answer

logger = logging.getLogger(__name__)

class LearningService:
    def __init__(self, repository):
        self.repository = repository
        
    async def prepare_picture_word(self) -> dict | None:
        """
        Получает слово с картинкой,
        сохраняет его в FSM.

        Возвращает слово,
        если оно найдено.
        """

        word = await self.repository.get_random_picture_word()

        if not word:
            return None 
        
        return word


    async def get_next_word(self, user_id: int, mode: str) -> dict | None:
        """
        Возвращает следующее слово в зависимости от режима обучения
        Если подходящего слова нет возвращает None
        """

        language = await self.repository.get_language(user_id)

        if not language:
            return None
        
        if mode == MODE_ERRORS:
            return await self.repository.get_random_wrong_word(user_id, language)
        
        if mode == MODE_REVIEW:
            return await self.repository.get_review_word(user_id, language)
        
        session = await self.repository.get_learning_session(user_id)

        if not session:
            return None
        
        return await self.repository.get_random_word(
            user_id,
            language,
            session["category"],
            session["level"],

        )


    # =====================
    # Сохранение результата
    # =====================

    async def save_word_result(
        self,
        user_id: int,
        word_id: int,
        correct: bool,
    ):
        """
        Сохраняет ответ пользователя
        и начисляет опыт.
        """
        logger.info(
            "Saving answer: user_id=%s, word_id =%s correct=%s",
            user_id,
            word_id,
            correct
        )

        try:
            await self.repository.save_word_answer(
                user_id,
                word_id,
                correct,
            )
        except Exception:
            logger.exception(
                "Failed to save answer: user_id=%s word_id=%s",
                user_id,
                word_id
            )
            raise   

        xp = calculate_study_xp(correct)

        logger.info(
            "XP calculated: user_id=%s xp=%s correct=%s",
            user_id,
            xp,
            correct
        )

        try:
            await self.repository.add_xp(user_id, xp)
        except Exception:
            logger.exception(
                "Failed to add XP: user_id=%s xp=%s",
                user_id,
                xp
            )
            raise   


         
    # =====================
    # Проверка ответа
    # =====================
    async def process_answer(
        self,
        user_id: int,
        word_id: int,
        mode: str,
        answer: str | None = None,
        correct: bool | None = None,
        update_session: bool = False,
    ) -> LearningResult:

        logger.info(
            "Processing answer: user_id=%s word_id=%s mode=%s",
            user_id,
            word_id,
            mode
        )

        word = await self.repository.get_word(word_id)

        if not word:
            logger.warning(
                "Word not found: user_id=%s word_id%s",
                user_id,
                word_id
            )
            return LearningResult(
                correct=False,
                next_word=None,
                finished=False,
                word=None,
            )

        if answer is not None:
            correct = check_answer(
                answer,
                word["translation"],
            )

        logger.info(
            "Answer processed: user_id=%s word_id=%s correct=%s",
            user_id,
            word_id,
            correct
        )
                        
        if correct is None:
            raise ValueError("Не передан answer или correct")

        await self.save_word_result(
            user_id=user_id,
            word_id=word_id,
            correct=correct,
        )

        if update_session:
            await self.repository.update_session_result(
                user_id=user_id,
                correct=correct,
            )

        next_word = await self.get_next_word(
            user_id=user_id,
            mode=mode,
        )

        return LearningResult(
            correct=correct,
            next_word=next_word,
            finished=next_word is None,
            word=word,
        )


    async def start_new_learning(
            self,  
            user_id: int,
            category: str,
            level: str,
    ) -> dict | None:

        logger.info(
            "Starting new learning: user_id=%s category=%s level=%s",
            user_id,
            category,
            level
        )

        language = await self.repository.get_language(user_id)

        if not language:
            logger.warning(
                "Language not found: user_id=%s",
                user_id
            )
            return None

        await self.repository.save_learning_session(
            user_id,
            category=category,
            level=level,
        )

        word = await self.repository.get_random_word(
            user_id=user_id,
            language=language,
            category=category,
            level=level,

        )

        if not word:
            logger.warning(
                "No words found: user_id=%s category=%s level=%s",
                user_id,
                category,
                level
            )
            return None

        await self.repository.add_word_progress(
            user_id,
            word["id"]
        )

        logger.info(
            "Learning started successfully: user_id=%s word_id=%s",
            user_id,
            word["id"]
        )

        return {
            "word": word,
            "mode": MODE_NEW,
        }

    async def finish_learning(self, user_id: int)-> dict | None:
        session = await self.repository.finish_session(user_id)

        if not session:
            return None

        return session

    async def get_word(self, word_id: int) -> dict | None:
        return await self.repository.get_word(word_id)

    async def process_picture_answer(
        self,
        user_id: int,
        word_id: int,
        answer: str,
    ) -> tuple[dict | None, bool | None]:

        word = await self.repository.get_word(word_id)

        if not word:
            return None, None

        correct = (
            answer.strip().lower()
            == word["word"].strip().lower()
        )

        await self.save_word_result(
            user_id=user_id,
            word_id=word_id,
            correct=correct,
        )

        return word, correct



        