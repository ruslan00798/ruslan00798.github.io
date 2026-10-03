from unittest.mock import AsyncMock

from services.history_service import HistoryService

async def test_get_translation_history():
    repository = AsyncMock()
    

    word = {
        "id": 10,
        "text": "Hello",
        "translation": "Привет",
    }

    repository.get_history_by_id.return_value = word

    service = HistoryService(repository)

    result = await service.get_translation_history(
        user_id=123,
        history_id=10,
    )

    assert result == word

    repository.get_history_by_id.assert_awaited_once_with(
    123,
    10,
    )


async def test_get_translation_history_not_found():
    repository = AsyncMock()

    repository.get_history_by_id.return_value = None

    service = HistoryService(repository)

    result = await service.get_translation_history(
        user_id=123,
        history_id=999,
    )

    assert result is None

    repository.get_history_by_id.assert_awaited_once_with(
        123,
        999,
    )

async def test_clear_user_history():
    repository = AsyncMock()

    repository.clear_history.return_value = True

    service = HistoryService(repository)

    result = await service.clear_user_history(user_id=123)

    assert result is True

    repository.clear_history.assert_awaited_once_with(123)

async def test_delete_user_history_item():
    repository = AsyncMock()

    repository.delete_history.return_value = True

    service = HistoryService(repository)

    result = await service.delete_user_history_item(user_id=123, history_id=999)

    assert result is True

    repository.delete_history.assert_awaited_once_with(123, 999)

async def test_not_delete_user_history_item():
    repository = AsyncMock()

    repository.delete_history.return_value = False

    service = HistoryService(repository)

    result = await service.delete_user_history_item(user_id=123, history_id=999)

    assert result is False

    repository.delete_history.assert_awaited_once_with(123, 999)


async def test_get_user_favorites():
    repository = AsyncMock()

    favorites_list = [
        {"id": 1, "text": "Hello", "translation": "Привет"},
        {"id": 2, "text": "Good morning", "translation": "Доброе утро"}
    ]

    repository.get_favorites.return_value = favorites_list

    service = HistoryService(repository)

    result = await service.get_user_favorites(user_id=123)

    assert result == favorites_list

    repository.get_favorites.assert_awaited_once_with(123)


async def test_toggle_user_favorite_add():
    repository = AsyncMock()

    repository.toggle_favorite.return_value = True

    service = HistoryService(repository)

    result = await service.toggle_user_favorite(user_id=123, history_id=999)

    assert result is True

    repository.toggle_favorite.assert_awaited_once_with(123, 999)
    
    
async def test_toggle_user_favorite_not_add():
    repository = AsyncMock()

    repository.toggle_favorite.return_value = False

    service = HistoryService(repository)

    result = await service.toggle_user_favorite(user_id=123, history_id=999)

    assert result is False

    repository.toggle_favorite.assert_awaited_once_with(123, 999)
    
    
async def test_toggle_user_favorite_is_None():
    repository = AsyncMock()

    repository.toggle_favorite.return_value = None

    service = HistoryService(repository)

    result = await service.toggle_user_favorite(user_id=123, history_id=999)

    assert result is None

    repository.toggle_favorite.assert_awaited_once_with(123, 999)

async def test_remove_user_favorite():
    repository = AsyncMock()

    repository.remove_favorite.return_value = False

    service = HistoryService(repository)

    result = await service.remove_user_favorite(
    user_id=123,
    history_id=999,
    )

    assert result is False

    repository.remove_favorite.assert_awaited_once_with(
    123,
    999,
    )

async def test_remove_user_favorite_not_found():
    repository = AsyncMock()

    repository.remove_favorite.return_value = None

    service = HistoryService(repository)

    result = await service.remove_user_favorite(user_id=123, history_id=999,)

    assert result is None

    repository.remove_favorite.assert_awaited_once_with(
    123,
    999,
    )

        





    


    

        

    

