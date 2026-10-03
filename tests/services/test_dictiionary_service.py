from unittest.mock import AsyncMock, patch

from services.dictionary_service import DictionaryService

async def test_find_word():
    repository = AsyncMock()
    history_service = AsyncMock()


    word = {
        "id": 10,
        "word": "hello",
        "language": "en"
    }

    repository.get_word.return_value = word

    service = DictionaryService(repository, history_service,)

    result = await service.find_word(
        word="hello",
        language="en"
    )

    assert result == word

    repository.get_word.assert_awaited_once_with(
        "hello",
        "en"
    )

async def test_get_or_create_word_existing():
    repository = AsyncMock()
    history_service = AsyncMock()

    word = {
        "id": 10,
        "word": "hello",
        "language": "en"
    }

    repository.get_word.return_value = word

    service = DictionaryService(repository, history_service)

    result = await service.get_or_create_word(
        word="hello",
        translation="привет",
        language="en"
    )

    assert result == 10

    repository.get_word.assert_awaited_once_with("hello", "en")
    repository.create_word.assert_not_awaited()

async def test_get_or_create_word_new():
    repository = AsyncMock()
    history_service = AsyncMock()

    repository.get_word.return_value = None
    repository.create_word.return_value = 25

    service = DictionaryService(repository, history_service,)

    result = await service.get_or_create_word(
        word="hello",
        translation="привет",
        language="en"
    )

    assert result == 25

    repository.get_word.assert_awaited_once_with(
        "hello",
        "en",
    )

    repository.create_word.assert_awaited_once_with(
        "hello",
        "привет",
        language="en",
        category="history",
        level="1"
    )


async def test_add_word_from_history_success():
    repository = AsyncMock()
    history_service = AsyncMock()

    history = {
        "original_text": "hello",
        "translated_text": "привет"
    }

    history_service.get_translation_history.return_value = history
    repository.get_language.return_value = "en"

    service = DictionaryService(
        repository,
        history_service
    )

    service.get_or_create_word = AsyncMock(return_value=25)

    result = await service.add_word_from_history(
        user_id=123,
        history_id=50
    )

    assert result == {
        "success": True,
        "word": "hello",
        "translation": "привет"
    }

    history_service.get_translation_history.assert_awaited_once_with(
        123,
        50
    )

    repository.get_language.assert_awaited_once_with(123)

    service.get_or_create_word.assert_awaited_once_with(
        "hello",
        "привет",
        "en"
    )

    repository.add_word_progress.assert_awaited_once_with(
        123,
        25
    )


async def test_add_word_from_history_not_found():
    repository = AsyncMock()
    history_service = AsyncMock()

    history_service.get_translation_history.return_value = None

    service = DictionaryService(
        repository,
        history_service,
    )

    result = await service.add_word_from_history(
        user_id=123,
        history_id=999,
    )

    assert result == {
        "success": False,
        "error": "history_not_found",
    }

    history_service.get_translation_history.assert_awaited_once_with(
        123,
        999,
    )
