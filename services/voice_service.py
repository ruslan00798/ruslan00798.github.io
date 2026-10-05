#voice.py

import os

from aiogram.types import Message, FSInputFile

from services.tts import generate_audio


async def send_word_voice(
    message: Message,
    word: dict,
):
    """
    Создаёт аудио и отправляет его.
    Возвращает message_id аудио.
    """

    if not word:
        return None

    text = word.get("word")

    if not text:
        return None

    language = word.get(
        "language",
        "en"
    )

    file_path = None

    try:

        file_path = await generate_audio(
            text=text,
            language=language,
        )

        audio_message = await message.answer_audio(
            audio=FSInputFile(file_path),
            caption=f"🔊 {text}",
        )

        return audio_message.message_id


    except Exception:

        return None


    finally:

        if file_path and os.path.exists(file_path):
            os.remove(file_path)