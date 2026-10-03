import pytest 
from unittest.mock import AsyncMock, patch 
from services.translation_service import TranslateService 
from models.translation import AudioResult, TranslationError

@pytest.mark.asyncio 
async def test_process_translation_empty_text(): 
    repository = AsyncMock()

    service = TranslateService(repository)

    result = await service.process_translation(
        user_id=123,
        text=" ",
    )
    assert result.error == TranslationError.EMPTY_TEXT

    repository.get_language.assert_not_awaited() 
    repository.get_word.assert_not_awaited() 
    repository.save_history.assert_not_awaited()

@pytest.mark.asyncio 
async def test_process_translation_language_not_selected():
    repository = AsyncMock()

    repository.get_language.return_value = None

    service = TranslateService(repository)

    result = await service.process_translation(user_id=123, text="hello",)

    assert result.error == TranslationError.LANGUAGE_NOT_SELECTED

    repository.get_language.assert_awaited_once_with(123) 
    repository.get_word.assert_not_awaited() 
    repository.save_history.assert_not_awaited()

@pytest.mark.asyncio 
async def test_process_translation_word_found_in_database(): 
    repository = AsyncMock()

    repository.get_language.return_value = "en"

    db_word = {
        "translation": "привет",
    }

    repository.get_word.return_value = db_word
    repository.save_history.return_value = 42

    with patch(
        "services.translation_service.translate"
    ) as mock_translate:

        service = TranslateService(repository)

        result = await service.process_translation(
            user_id=123,
            text="hello",
        )

        assert result.translated == "привет" 
        assert result.history_id == 42 
        assert result.error is None 
        repository.get_language.assert_awaited_once_with(123) 
        repository.get_word.assert_awaited_once_with( "hello", "en", ) 
        repository.save_history.assert_awaited_once_with( 123, "hello", "привет", ) 
        mock_translate.assert_not_awaited()

@pytest.mark.asyncio 
async def test_process_translation_word_not_found_uses_translator(): 
    repository = AsyncMock()

    repository.get_language.return_value = "en"
    repository.get_word.return_value = None
    repository.save_history.return_value = 42

    with patch(
        "services.translation_service.translate"
    ) as mock_translate:

        mock_translate.return_value = "привет"

        service = TranslateService(repository)

        result = await service.process_translation(
            user_id=123,
            text="hello",
        )

    assert result.translated == "привет"
    assert result.history_id == 42
    assert result.error is None

    repository.get_language.assert_awaited_once_with(123) 
    repository.get_word.assert_awaited_once_with( "hello", "en", ) 
    mock_translate.assert_awaited_once_with( "hello", "en", ) 
    repository.save_history.assert_awaited_once_with( 123, "hello", "привет", )


@pytest.mark.asyncio
async def test_process_translation_translation_failed():
    repository = AsyncMock()

    repository.get_language.return_value = "en"
    repository.get_word.return_value = None

    with patch(
        "services.translation_service.translate"
    ) as mock_translate:

        mock_translate.return_value = None

        service = TranslateService(repository)

        result = await service.process_translation(
            user_id=123,
            text="hello",
        )

    assert result.error == TranslationError.TRANSLATION_FAILED

    repository.get_language.assert_awaited_once_with(123)

    repository.get_word.assert_awaited_once_with(
        "hello",
        "en",
    )

    mock_translate.assert_awaited_once_with(
        "hello",
        "en",
    )

    repository.save_history.assert_not_awaited()

@pytest.mark.asyncio
async def test_process_translation_arabic_adds_harakat():
    repository = AsyncMock()

    repository.get_language.return_value = "ar"
    repository.get_word.return_value = None
    repository.save_history.return_value = 42

    with (
        patch(
            "services.translation_service.translate"
        ) as mock_translate,
        patch(
            "services.translation_service.add_harakat_simple"
        ) as mock_add_harakat,
    ):
        mock_translate.return_value = "مرحبا"
        mock_add_harakat.return_value = "مَرْحَبًا"

        service = TranslateService(repository)

        result = await service.process_translation(
            user_id=123,
            text="hello",
        )

    assert result.translated == "مَرْحَبًا"
    assert result.history_id == 42
    assert result.error is None

    repository.get_language.assert_awaited_once_with(123)

    repository.get_word.assert_awaited_once_with(
        "hello",
        "ar",
    )

    mock_translate.assert_awaited_once_with(
        "hello",
        "ar",
    )

    mock_add_harakat.assert_called_once_with(
        "مرحبا",
    )

    repository.save_history.assert_awaited_once_with(
        123,
        "hello",
        "مَرْحَبًا",
    )

@pytest.mark.asyncio 
async def test_get_translation_for_repeat_history_found(): 
    repository = AsyncMock()

    history = {
        "id": 10,
        "translated_text": "Привет",
    }
    repository.get_history_by_id.return_value = history

    service = TranslateService(repository)

    result = await service.get_translation_for_repeat(
        user_id=123,
        history_id=10,
    )

    assert result is not None
    assert result.id == 10
    assert result.translated_text == "Привет"

    repository.get_history_by_id.assert_awaited_once_with(
        123,
        10
    )

@pytest.mark.asyncio 
async def test_get_translation_for_repeat_history_not_found(): 
    repository = AsyncMock()

    repository.get_history_by_id.return_value = None

    service = TranslateService(repository)

    result = await service.get_translation_for_repeat(
        user_id=123,
        history_id=10,
    )

    assert result is None

    repository.get_history_by_id.assert_awaited_once_with(
        123,
        10
    )

@pytest.mark.asyncio
async def test_get_audio_for_history_history_not_found():
    repository = AsyncMock()
    repository.get_history_by_id.return_value = None

    service = TranslateService(repository)

    result = await service.get_audio_for_history(
        user_id=123,
        history_id=456,
    )

    assert result is None

    repository.get_history_by_id.assert_awaited_once_with(
        123,
        456,
    )

@pytest.mark.asyncio
async def test_get_audio_for_history_not_found_language():
    repository = AsyncMock()

    history = {
        "id": 456,
        "translated_text": "مرحبا",
    }
    repository.get_history_by_id.return_value = history
    repository.get_language.return_value = None

    service = TranslateService(repository)

    result = await service.get_audio_for_history(
        user_id=123,
        history_id=456,
    )

    assert result is None

    repository.get_history_by_id.assert_awaited_once_with( 123, 456, ) 
    repository.get_language.assert_awaited_once_with( 123, )


@pytest.mark.asyncio
async def test_get_audio_for_history_audio_generation_failed():
    # Arrange
    repository = AsyncMock()
    service = TranslateService(repository)

    repository.get_history_by_id.return_value = {
        "id": 456,
        "translated_text": "مرحبا",
    }

    repository.get_language.return_value = "ar"

    with patch(
        "services.translation_service.generate_audio",
        new_callable=AsyncMock,
    ) as mock_generate_audio:

        mock_generate_audio.return_value = None

        # Act
        result = await service.get_audio_for_history(
            user_id=123,
            history_id=456,
        )

    # Assert
    assert result is None

    repository.get_history_by_id.assert_awaited_once_with(
        123,
        456,
    )

    repository.get_language.assert_awaited_once_with(
        123,
    )

    mock_generate_audio.assert_awaited_once_with(
        "مرحبا",
        "ar",
    )

@pytest.mark.asyncio 
async def test_get_audio_for_history_success():
    repository = AsyncMock()
    service = TranslateService(repository)

    history = {
        "id": 456, 
        "translated_text": "مرحبا",
    }
    repository.get_history_by_id.return_value = history
    repository.get_language.return_value = "ar"

    with patch(
        "services.translation_service.generate_audio",
        new_callable=AsyncMock,
    ) as mock_generate_audio:

        mock_generate_audio.return_value = "/tmp/audio.mp3"

        result = await service.get_audio_for_history(
            user_id=123,
            history_id=456,
        )

    assert isinstance(result, AudioResult)

    assert result.file_path == "/tmp/audio.mp3" 
    assert result.text == "مرحبا" 
    repository.get_history_by_id.assert_awaited_once_with( 123, 456, ) 
    repository.get_language.assert_awaited_once_with( 123, ) 
    mock_generate_audio.assert_awaited_once_with( "مرحبا", "ar", )    


   
