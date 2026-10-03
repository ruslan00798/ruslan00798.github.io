from database.requests import (
    update_language,
    update_daily_goal,
    get_language,
)


class LanguageRepository:

    async def update_language(
        self,
        user_id: int,
        language_code: str,
    ):
        return await update_language(
            user_id,
            language_code,
        )

    async def update_daily_goal(
        self,
        user_id: int,
        daily_goal: int,
    ):
        return await update_daily_goal(
            user_id,
            daily_goal,
        )

    async def get_language(
        self,
        user_id: int,
    ):
        return await get_language(user_id)