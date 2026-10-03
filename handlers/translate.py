#translate.py

import logging
import os

from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile, Message

from filters.history_data import RepeatCallback, VoiceHistoryCallback
from keyboards.translate_kbd import translate_keyboard
from services.learning.translate_repository import TranslateRepository
from services.translation_service import TranslateService
   
from services.word_sender import handle_translation_error
from states.translate_state import TranslateState

translate_repository = TranslateRepository()
translate_service = TranslateService(translate_repository)

logger = logging.getLogger(__name__)

translate_router = Router()

MAX_MESSAGE_LENGTH = 5000


# ==========================
# Перевод текста
# ==========================

@translate_router.message(TranslateState.waiting_text, F.text,)
async def translate_text(message: Message):
    user_id = message.from_user.id
    text = message.text

    logger.info(
        "translation_started user_id=%s text_length=%s",
        user_id,
        len(text),
    )

    if len(text) > MAX_MESSAGE_LENGTH:
        logger.warning(
            "translation_text_too_long user_id=%s text_lenght=%s max_lenght=%s",
            user_id,
            len(text),
            MAX_MESSAGE_LENGTH,
        )

        await message.answer(
            f"❌ Максимальная длина текста — {MAX_MESSAGE_LENGTH} символов."
        )
        return

    try:
        result = await translate_service.process_translation(
            user_id=user_id,
            text=text,
        )

    except Exception:
        logger.exception(
            "Ошибка при переводе текста: user=%s",
            user_id,
        )

        await message.answer(
            "❌ Ошибка перевода."
        )
        return

    if not result.success:
        logger.warning(
            "translation_rejected user_id=%s error=%s",
            user_id,
            result.error,
        )

        await handle_translation_error(
            message,
            result.error,
        )
        return

    logger.info(
        "translation_completed user_id=%s history_id=%s",
        user_id,
        result.history_id,
    )

    await message.answer(
        "🌍 Перевод:\n\n"
        f"{result.translated}",
        reply_markup=translate_keyboard(
            result.history_id,
        ),
    )


# ==========================
# Повторить перевод
# ==========================

@translate_router.callback_query(RepeatCallback.filter(),)
async def repeat_translation(
    callback: CallbackQuery,
    callback_data: RepeatCallback,
):
    user_id = callback.from_user.id
    history_id=callback_data.id

    logger.info(
        "translation_repeat_started user_id=%s history_id=%s",
        user_id,
        history_id,
    )


    history = await translate_service.get_translation_for_repeat(
        user_id=user_id,
        history_id=history_id,
    )

    if not history:
        logger.warning(
            "translation_repeat_not_found user_id=%s history_id=%s",
            user_id,
            history_id,
        )

        await callback.answer(
            "❌ Перевод не найден.",
            show_alert=True,
        )
        return

    if not callback.message:
        logger.error(
            "translation_repeat_no_message user_id=%s history_id=%s",
            user_id,
            history_id,
        )

        await callback.answer(
            "❌ Не удалось отправить перевод.",
            show_alert=True,
        )
        return

    await callback.message.answer(
        "🌍 Перевод:\n\n"
        f"{history.translated_text}",
        reply_markup=translate_keyboard(
            history.id,
        ),
    )

    logger.info(
        "translation_repeat_completed user_id=%s history_id=%s",
        user_id,
        history_id,
    )


    await callback.answer()


# =========================
# Прослушать перевод
# =========================

@translate_router.callback_query(VoiceHistoryCallback.filter(),)
async def play_translation_voice(
    callback: CallbackQuery,
    callback_data: VoiceHistoryCallback,
):
    user_id = callback.from_user.id
    history_id = callback_data.id

    logger.info(
        "translation_voice_started user_id=%s history_id=%s",
        user_id,
        history_id,
    )

    result = await translate_service.get_audio_for_history(
        user_id=user_id,
        history_id=history_id,
    )

    if not result:
        logger.warning(
            "translation_voice_not_found user_id=%s history_id=%s",
            user_id,
            history_id,
        )
        await callback.answer(
            "❌ Не удалось получить аудио.",
            show_alert=True,
        )
        return

    if not callback.message:
        await callback.answer(
            "❌ Не удалось отправить аудио.",
            show_alert=True,
        )

        try:
            os.remove(result.file_path)
        except FileNotFoundError:
            pass
        except OSError:
            logger.exception(
                "Не удалось удалить временный файл: %s",
                result.file_path,
            )

        return

    try:
        await callback.message.answer_audio(
            audio=FSInputFile(result.file_path),
            caption=f"🔊 {result.text}",
        )

    except Exception:
        logger.exception(
            "Ошибка отправки аудио: user=%s history_id=%s",
            user_id,
            history_id,
        )

        await callback.answer(
            "❌ Не удалось отправить аудио.",
            show_alert=True,
        )

    else:
        logger.info(
            "Аудио успешно отправлено: user=%s history_id=%s",
            user_id,
            history_id,
        )

        await callback.answer()

    finally:
        try:
            os.remove(result.file_path)
        except FileNotFoundError:
            pass
        except OSError:
            logger.exception(
                "Не удалось удалить временный файл: %s",
                result.file_path,
            )