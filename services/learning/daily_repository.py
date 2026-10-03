from database.requests import (
    add_xp,
    update_daily_goal,
    update_streak,
    get_language
)

class DailyLoginRepository:
    async def get_language(self, user_id: int):
        return await get_language(user_id)
    
    async def update_streak(self, user_id: int):
        return await update_streak(user_id)

    async def update_daily_goal(self, user_id: int):
        return await update_daily_goal(user_id)

    async def add_xp(
        self,
        user_id: int,
        xp: int,
    ):
        return await add_xp(user_id, xp)