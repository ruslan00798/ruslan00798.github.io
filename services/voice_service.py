import os

from aiogram.types import CallbackQuery, FSInputFile

from services.tts import get_voice, text_to_speech
from database.requests import get_voice_setting


async def send_word_voice(callback: CallbackQuery, word: dict,):

    voice_enabled = await get_voice_setting(callback.from_user.id)

    if not voice_enabled:
        return
    
    language = word.get("language", "en")

    file_path = await text_to_speech(
        word["word"],
        get_voice(language)
    )

    await callback.message.answer_audio(
        audio=FSInputFile(file_path),
        caption=f"🔊 {word['word']}"
    )

    os.remove(file_path)
