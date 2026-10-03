from database.requests import (
    get_history,
    get_history_by_id,
    clear_history,
    delete_history,
    get_favorites,
    toggle_favorite,
    remove_favorite
)


class HistoryRepository():

    async def get_history(
        self,
        user_id,
        limit,
        offset
    ):
        return await get_history(
            user_id,
            limit,
            offset
        )

    async def get_history_by_id(self,  user_id, history_id):
        return await get_history_by_id( user_id, history_id)

    async def clear_history(self, user_id):
        return await clear_history(user_id)

    async def delete_history(self, user_id, history_id):
        return await delete_history(user_id, history_id)

    async def get_favorites(self, user_id):
        return await get_favorites(user_id)

    async def toggle_favorite(self, user_id, history_id):
        return await toggle_favorite(user_id, history_id)

    async def remove_favorite(self, user_id, history_id):
        return await remove_favorite(user_id, history_id)