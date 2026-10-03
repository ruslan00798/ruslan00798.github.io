import logging

HISTORY_PAGE_SIZE = 5

logger = logging.getLogger(__name__)

class HistoryService:
    def __init__(self, repository):
        self.repository = repository

    async def get_history_page(
        self,
        user_id: int,
        page: int,
    ) -> tuple[list, bool]:
        """
        Возвращает страницу истории переводов пользователя.
        """

        offset = page * HISTORY_PAGE_SIZE
        limit = HISTORY_PAGE_SIZE + 1

        logger.info(
            "Получаем страницу истории: user_id=%s page=%s limit=%s offset=%s",
            user_id,
            page,
            limit,
            offset,
        )

        try:
            history = await self.repository.get_history(
                user_id=user_id,
                limit=limit,
                offset=offset,
            )

            has_next = len(history) > HISTORY_PAGE_SIZE
            history_page = history[:HISTORY_PAGE_SIZE]

            logger.info(
                "History page received: user_id=%s page=%s items=%s has_next=%s",
                user_id,
                page,
                len(history_page),
                has_next,
            )

            return history_page, has_next

        except Exception:
            logger.exception(
                "Failed to get history page user_id=%s page=%s",
                user_id,
                page,
            )
            raise


    async def get_translation_history(self,user_id: int, history_id: int):
        """
        Получает один перевод из истории.
        """
        logger.info(
            "Получение элемента из истории: user_id=%s history_id=%s",
            user_id,
            history_id,
        )

        try:
            result = await self.repository.get_history_by_id(
                user_id, history_id
            )

            logger.info(
                "получили элемент истории: user_id=%s history_id=%s"
                "found=%s",
                user_id,
                history_id,
                result is not None
            )
            return result

        except Exception:
            logger.exception(
                "не удалось получить элемент истории user_id=%s history_id=%s",
                user_id,
                history_id,
            )
            raise

    async def clear_user_history(self,user_id: int,):
        """
        Очищает историю пользователя.
        """
        logger.info(
            "очищение истории пользователя user_id=%s",
            user_id,
        )
        try:
            result = await self.repository.clear_history(user_id)

            logger.info(
                "Историю пользователь очистил user_id=%s result=%s",
                user_id,
                result,
            )
            return result

        except Exception:
            logger.exception(
                "очистить историю пользователя не удалось user_id=%s",
                user_id
            )
            raise


    async def delete_user_history_item(self,user_id: int, history_id: int,) -> bool:
        """
        Удаляет один перевод.
        """
        logger.info(
            "удаление элемента истории user_id=%s history_id=%s",
            user_id,
            history_id,
        )

        try:
            deleted = await self.repository.delete_history(user_id, history_id,)

            logger.info(
                "Удаление элемента истории завершено user_id=%s history_id=%s result=%s",
                user_id,
                history_id,
                deleted
            )
            return deleted

        except Exception:
            logger.exception(
                "не удалось удалить элемент истории user_id=%s history_id=%s",
                user_id,
                history_id,
            )
            raise    


    async def get_user_favorites(self,user_id: int):
        logger.info(
            "получение избранных переводов: user_id=%s",
            user_id,
        )
        try:
            favorites = await self.repository.get_favorites(user_id)

            logger.info(
                "получили избранное пользователя: user_id=%s count=%s",
                user_id,
                len(favorites)
            )
            return favorites

        except Exception:
            logger.exception(
                "Не удалось получить избранное пользователя user_id=%s",
                user_id,
            )
            raise

    async def toggle_user_favorite(self,user_id: int, history_id: int,) -> bool | None:
        """
        Добавляет или убирает избранное.
        """
        logger.info(
            "добавить избранное user_id=%s history_id=%s",
            user_id,
            history_id,
        )
        try:
            result  = await self.repository.toggle_favorite(user_id, history_id)

            logger.info(
                "добавление избранного завершено user_id=%s history_id=%s result=%s",
                user_id,
                history_id,
                result 
            )
            return result
        except Exception:
            logger.exception(
                "ну удалось добавить в избранное user_id=%s history_id=%s",
                user_id,
                history_id,
            )
            raise


    async def remove_user_favorite(self,user_id: int, history_id: int) -> bool | None:

        """
        Убирает перевод из избранного.
        """
        logger.info(
            "убираем перевод из избранного user_id=%s history_id=%s",
            user_id,
            history_id,
        )

        try:
            result = await self.repository.remove_favorite(user_id, history_id)

            logger.info(
                "Удаление избранного завершено: user_id=%s history_id=%s result=%s",
                user_id,
                history_id,
                result
            )
            return result

        except Exception:
            logger.exception(
                "не удалось удалить избранное user_id=%s history_id=%s",
                user_id,
                history_id,
            )
            raise