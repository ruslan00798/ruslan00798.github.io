from database.requests import (
    get_statistics,
    get_xp,
    get_learned_words,
    get_language,
    get_daily_goal,
    get_study_progress
)

class ProfileRepository:
    async def get_statistics(self, user_id):
        return await get_statistics(user_id)

    async def get_xp(self, user_id):
        return await get_xp(user_id)

    async def get_learned_words(self, user_id):
        return await get_learned_words(user_id)

    async def get_language(self, user_id):
        return await get_language(user_id)

    async def get_daily_goal(self, user_id):
        return await get_daily_goal(user_id)

    async def get_study_progress(self, user_id):
        return await get_study_progress(user_id)

