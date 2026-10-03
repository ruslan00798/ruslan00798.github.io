import logging

logger = logging.getLogger(__name__)


from services.learning.language_repository import LanguageRepository

class LanguageService:
    def __init__(self, repository: LanguageRepository):
        self.repository = repository

    async def change_language(
        self,
        user_id: int,
        language_code: str,
        daily_goal: int,    
    ):
        logger.info(
            "обновляем язык: user_id=%s language_code=%s daily_goal=%s",
            user_id,
            language_code,
            daily_goal,
        )

        try:
            language = await self.repository.update_language(
                user_id,
                language_code,
            )

            updated_goal = await self.repository.update_daily_goal(
                user_id,
                daily_goal,
            )

            logger.info(
                "обновление языка и цели user_id=%s language_code=%s",
                user_id,
                language_code,
                updated_goal,
            )
            return language, updated_goal
        
        except Exception:
            logger.exception(
                "не удалось изменить язык и цель user_id=%s language_code=%s dayly_goal=%s",
                user_id,
                language_code,
                daily_goal,
            )
            raise
        
            
