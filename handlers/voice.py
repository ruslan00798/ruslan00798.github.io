import os

from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from database.requests import get_word_by_id
from services.tts import generate_audio


voice_router = Router()


# =====================================
# Голос
# =====================================


@voice_router.callback_query(F.data.startswith("voice:"))
async def play_voice(callback: CallbackQuery):

    await callback.answer()

    word_id = int(callback.data.split(":")[1])


    word = await get_word_by_id(word_id)


    if not word:
        await callback.message.answer("❌ Слово не найдено")

        return


    file_path = await generate_audio(
        text=word["word"],
        language=word["language"]
    )

    await callback.message.answer_audio(
        audio=FSInputFile(file_path),
        caption=f"🔊 {word['word']}"
    )

    os.remove(file_path)