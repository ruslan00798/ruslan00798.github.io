#daily_login_ser
import logging

from utils.xp import (
    get_xp_reward,
    DAILY_LOGIN_ACTION,
)

logger = logging.getLogger(__name__)

class DailyLoginService:

    def __init__(self, repository):
        self.repository = repository

    async def get_language(self, user_id: int):
        logger.debug(
            "Получение языка пользователя: user_id=%s",
            user_id,
        )
        return await self.repository.get_language(user_id)    


    async def process_daily_login(self, user_id: int) -> dict | None:

        logger.info(
            "Обработка ежедневного входа: user_id=%s",
            user_id
        )
        try:
            streak, is_new_day = await self.repository.update_streak(user_id)
            
            logger.debug(
                "Обновлен streak: user_id=%s streak=%s is_new_day=%s",
                user_id,
                streak,
                is_new_day
            )
            
            await self.repository.update_daily_goal(user_id)

            logger.debug(
                "Обновлена ежедневная цель: user_id=%s",
                user_id
            )

            if not is_new_day:
                logger.info(
                    "Повторный вход в течение текущего дня: user_id=%s",
                    user_id,
                )
                return None
            
            xp = get_xp_reward(DAILY_LOGIN_ACTION)

            logger.debug(
                "Рассчитана награда за ежедневный вход: "
                "user_id=%s xp=%s",
                user_id,
                xp,
            )

            
            await self.repository.add_xp(user_id, xp)


            logger.info(
                "XP начислен за ежедневный вход: "
                "user_id=%s xp=%s streak=%s",
                user_id,
                xp,
                streak,
            )
            
            return {
            "streak": streak,
            "xp": xp,  
            }
        except Exception:
            logger.exception(
                "Ошибка при обработке ежедневного входа: user_id=%s",
                user_id,
            )
            raise    