import os 
from unittest.mock import AsyncMock, MagicMock, patch 
import pytest 
from services.voice_service import send_word_voice

@pytest.mark.asyncio
async def test_send_word_voice_returns_none_when_word_is_empty():
    message = MagicMock()

    result = await send_word_voice(message, {})

    assert result is None
    message.answer_audio.assert_not_called()

@pytest.mark.asyncio
async def test_send_word_voice_returns_none_when_word_text_is_missing():
    message = MagicMock()

    result = await send_word_voice(
        message,
        {"language": "en"},
    )

    assert result is None
    message.answer_audio.assert_not_called()

@pytest.mark.asyncio
async def test_send_word_voice_sends_audio_and_returns_message_id():
    message = MagicMock()

    audio_message = MagicMock()
    audio_message.message_id = 123

    message.answer_audio = AsyncMock(
        return_value=audio_message
    )

    file_path = "/tmp/hello.mp3"

    with (
        patch(
            "services.voice_service.generate_audio",
            new_callable=AsyncMock,
            return_value=file_path,
        ) as mock_generate_audio,
        patch(
            "services.voice_service.FSInputFile"
        ) as mock_fs_input_file,
        patch(
            "services.voice_service.os.path.exists",
            return_value=True,
        ),
        patch(
            "services.voice_service.os.remove"
        ) as mock_remove,
    ):
        result = await send_word_voice(
            message,
            {
                "word": "hello",
                "language": "en",
            },
        )

    assert result == 123

    mock_generate_audio.assert_awaited_once_with(
        text="hello",
        language="en",
    )

    mock_fs_input_file.assert_called_once_with(file_path)

    message.answer_audio.assert_awaited_once_with(
        audio=mock_fs_input_file.return_value,
        caption="🔊 hello",
    )

    mock_remove.assert_called_once_with(file_path)

@pytest.mark.asyncio
async def test_send_word_voice_uses_english_by_default():
    message = MagicMock()

    audio_message = MagicMock()
    audio_message.message_id = 123

    message.answer_audio = AsyncMock(
        return_value=audio_message
    )

    file_path = "/tmp/hello.mp3"

    with (
        patch(
            "services.voice_service.generate_audio",
            new_callable=AsyncMock,
            return_value=file_path,
        ) as mock_generate_audio,
        patch("services.voice_service.FSInputFile"),
        patch(
            "services.voice_service.os.path.exists",
            return_value=True,
        ),
        patch("services.voice_service.os.remove"),
    ):
        result = await send_word_voice(
            message,
            {"word": "hello"},
        )

    assert result == 123

    mock_generate_audio.assert_awaited_once_with(
        text="hello",
        language="en",
    )

@pytest.mark.asyncio
async def test_send_word_voice_returns_none_when_generate_audio_fails():
    message = MagicMock()
    message.answer_audio = AsyncMock()

    with patch(
        "services.voice_service.generate_audio",
        new_callable=AsyncMock,
        side_effect=Exception("TTS error"),
    ):
        result = await send_word_voice(
            message,
            {
                "word": "hello",
                "language": "en",
            },
        )

    assert result is None
    message.answer_audio.assert_not_awaited()    

@pytest.mark.asyncio
async def test_send_word_voice_returns_none_when_sending_audio_fails():
    message = MagicMock()

    message.answer_audio = AsyncMock(
        side_effect=Exception("Telegram error")
    )

    file_path = "/tmp/hello.mp3"

    with (
        patch(
            "services.voice_service.generate_audio",
            new_callable=AsyncMock,
            return_value=file_path,
        ) as mock_generate_audio,
        patch(
            "services.voice_service.FSInputFile"
        ) as mock_fs_input_file,
        patch(
            "services.voice_service.os.path.exists",
            return_value=True,
        ),
        patch(
            "services.voice_service.os.remove"
        ) as mock_remove,
    ):
        result = await send_word_voice(
            message,
            {
                "word": "hello",
                "language": "en",
            },
        )

    assert result is None

    mock_generate_audio.assert_awaited_once_with(
        text="hello",
        language="en",
    )

    mock_remove.assert_called_once_with(file_path)

@pytest.mark.asyncio
async def test_send_word_voice_removes_file_when_generate_audio_succeeds():
    message = MagicMock()

    audio_message = MagicMock()
    audio_message.message_id = 42

    message.answer_audio = AsyncMock(
        return_value=audio_message
    )

    file_path = "/tmp/test.mp3"

    with (
        patch(
            "services.voice_service.generate_audio",
            new_callable=AsyncMock,
            return_value=file_path,
        ),
        patch(
            "services.voice_service.FSInputFile"
        ),
        patch(
            "services.voice_service.os.path.exists",
            return_value=True,
        ) as mock_exists,
        patch(
            "services.voice_service.os.remove"
        ) as mock_remove,
    ):
        result = await send_word_voice(
            message,
            {
                "word": "test",
                "language": "de",
            },
        )

    assert result == 42

    mock_exists.assert_called_once_with(file_path)
    mock_remove.assert_called_once_with(file_path)

@pytest.mark.asyncio
async def test_send_word_voice_does_not_remove_file_when_it_does_not_exist():
    message = MagicMock()

    audio_message = MagicMock()
    audio_message.message_id = 42

    message.answer_audio = AsyncMock(
        return_value=audio_message
    )

    file_path = "/tmp/test.mp3"

    with (
        patch(
            "services.voice_service.generate_audio",
            new_callable=AsyncMock,
            return_value=file_path,
        ),
        patch(
            "services.voice_service.FSInputFile"
        ),
        patch(
            "services.voice_service.os.path.exists",
            return_value=False,
        ),
        patch(
            "services.voice_service.os.remove"
        ) as mock_remove,
    ):
        result = await send_word_voice(
            message,
            {"word": "test"},
        )

    assert result == 42
    mock_remove.assert_not_called()            