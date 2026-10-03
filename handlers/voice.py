#voice.py
import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from filters.history_data import VoiceCallback
from services.learning.repository import LearningRepository
from services.learning_service import LearningService
from services.voice_service import send_word_voice


learning_repository = LearningRepository()
learning_service = LearningService(learning_repository)

voice_router = Router()

logger = logging.getLogger(__name__)


@voice_router.callback_query(VoiceCallback.filter())
async def play_voice(callback: CallbackQuery, callback_data: VoiceCallback):

    user_id = callback.from_user.id
    word_id = callback_data.word_id

    logger.info(
        "word_voice_started user_id=%s word_id=%s",
        user_id,
        word_id,
    )

    try:
        word = await learning_service.get_word(word_id)

    except Exception:
        logger.exception(
            "word_voice_get_word_failed user_id=%s word_id=%s",
            user_id,
            word_id,
        )

        await callback.answer(
            "❌ Не удалось получить слово.",
            show_alert=True,
        )
        return

    if not word:
        logger.warning(
            "word_voice_not_found user_id=%s word_id=%s",
            user_id,
            word_id,
        )

        await callback.answer(
            "❌ Слово не найдено.",
            show_alert=True,
        )
        return

    try:
        await send_word_voice(
            message=callback.message,
            word=word,
            user_id=user_id,
        )

    except Exception:
        logger.exception(
            "word_voice_send_failed user_id=%s word_id=%s",
            user_id,
            word_id,
        )

        await callback.answer(
            "❌ Не удалось озвучить слово.",
            show_alert=True,
        )
        return

    await callback.answer("🔊")

    logger.info(
        "word_voice_completed user_id=%s word_id=%s",
        user_id,
        word_id,
    )