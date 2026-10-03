from database.requests import get_language

class DocumentRepository:

    async def get_language(self, user_id:int):
        return await get_language(user_id)