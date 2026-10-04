import logging

from services.learning.language_repository import LanguageRepository


logger = logging.getLogger(__name__)


class LanguageService:
    def __init__(self, repository: LanguageRepository):
        self.repository = repository

    async def change_language(
        self,
        user_id: int,
        language_code: str,
    ):
        logger.info(
            "обновляем язык: user_id=%s language_code=%s",
            user_id,
            language_code,
        )

        try:
            language = await self.repository.update_language(
                user_id,
                language_code,
            )

            logger.info(
                "язык успешно обновлён: user_id=%s language_code=%s",
                user_id,
                language_code,
            )

            return language

        except Exception:
            logger.exception(
                "не удалось изменить язык: user_id=%s language_code=%s",
                user_id,
                language_code,
            )
            raise

    async def change_daily_goal(
        self,
        user_id: int,
        daily_goal: int,
    ):
        logger.info(
            "обновляем дневную цель: user_id=%s daily_goal=%s",
            user_id,
            daily_goal,
        )

        try:
            updated_goal = await self.repository.update_daily_goal(
                user_id,
                daily_goal,
            )

            logger.info(
                "дневная цель успешно обновлена: user_id=%s daily_goal=%s",
                user_id,
                daily_goal,
            )

            return updated_goal

        except Exception:
            logger.exception(
                "не удалось изменить дневную цель: "
                "user_id=%s daily_goal=%s",
                user_id,
                daily_goal,
            )
            raise