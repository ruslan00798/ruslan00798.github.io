import logging

from database.requests import (
    add_xp,
    finish_session,
    get_language,
    get_learning_session,
    get_random_word,
    get_random_wrong_word,
    get_review_word,
    save_word_answer,
    get_random_picture_word,
    update_session_result,
    get_word_by_id,
    save_learning_session,
    add_word_progress,
)

logger = logging.getLogger(__name__)

class LearningRepository:

    async def get_language(self, user_id: int):
        return await get_language(user_id)

    async def get_learning_session(self, user_id: int):
        return await get_learning_session(user_id)

    async def get_random_word(
        self,
        user_id: int,
        language: str,
        category: str,
        level: str,
    ):

        return await get_random_word(
            user_id=user_id,
            language=language,
            category=category,
            level=level,
        )

    async def get_random_wrong_word(
            self,
            user_id: int,
            language: int,
    ):
        return await get_random_wrong_word(
            user_id,
            language,
        )

    async def get_review_word(
            self,
            user_id: int,
            language: str,
    ):
        return await get_review_word(
            user_id,
            language,
        )

    async def get_word(self, word_id: int):
        return await get_word_by_id(word_id)

    async def save_word_answer(
            self,
            user_id: int,
            word_id: int,
            correct: bool,
    ):
        try:
            return await save_word_answer(
                user_id,
                word_id,
                correct
            )
        except Exception:
            logger.exception(
                "Failed to save word answer: user_id=%s word_id=%s correct=%s",
                user_id,
                word_id,
                correct
            )
            raise

    async def add_xp(
            self,
            user_id: int,
            xp: int,
    ):
        try:
            return await add_xp(user_id, xp)
        except Exception:
            logger.exception(
                "Failed to add XP: user_id=%s xp=%s",
                user_id,
                xp
            )
            raise

    async def update_session_result(
            self,
            user_id:int,
            correct: bool,
    ):
        try:
            return await update_session_result(
                user_id=user_id,
                correct=correct,
            )
        except Exception:
            logger.exception(
                "Failed to update learning session: user_id=%s correct=%s",
                user_id,
                correct
            )
            raise

    async def save_learning_session(
            self,
            user_id: int,
            category: str,
            level: str,
    ):
        return await save_learning_session(
            user_id,
            category=category,
            level=level
        )

    async def add_word_progress(
            self,
            user_id: int,
            word_id: int,
    ):
        return await add_word_progress(
            user_id,
            word_id
        )

    async def finish_session(self, user_id: int):
        return await finish_session(user_id)

    async def get_random_picture_word(self):
        return await get_random_picture_word()