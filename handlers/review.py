#review.py

import logging
import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.back_menu_kbd import back_menu_keyboard

from services.learning.constants import MODE_ERRORS, MODE_REVIEW

from services.learning.repository import LearningRepository
from services.learning_service import LearningService
from services.message_service import cleanup_word_message
from services.word_sender import (
    send_study_word,
    get_finish_message,
    get_mode_title,
)

learning_repository = LearningRepository()
learning_service = LearningService(learning_repository)


review_router = Router()
logger = logging.getLogger(__name__)


# =====================================
# Повторение ошибок
# =====================================

@review_router.callback_query(F.data == "repeat_errors")
async def repeat_errors(
    callback: CallbackQuery,
    state: FSMContext,
):

    user_id = callback.from_user.id

    logger.info(
        "review_errors_started user_id=%s",
        user_id,
    )

    await state.update_data(
        mode=MODE_ERRORS,
    )

    word = await learning_service.get_next_word(
        user_id=callback.from_user.id,
        mode=MODE_ERRORS,
    )

    if not word:
        logger.info(
            "review_errors_finished_no_words user=%s",
            user_id,
        )

        await callback.message.answer(
            get_finish_message(MODE_ERRORS),
            reply_markup=back_menu_keyboard(),
        )

        await callback.answer()
        return

    # asyncpg.Record -> получаем id через ключ
    word_id = word["id"]

    logger.info(
        "review_errors_word_selected user_id=%s word_id=%s",
        user_id,
        word_id,
    )

    audio_message_id = await send_study_word(
        callback.message,
        word,
        title=get_mode_title(MODE_ERRORS),
    )

    await state.update_data(
        audio_message_id=audio_message_id,
    )

    logger.info(
        "review_errors_started_word_sent user_id=%s word_id=%s audio_message_id=%s",
        user_id,
        word_id,
        audio_message_id,
    )

    await callback.answer()


# =====================================
# Повторение изученных слов
# =====================================

@review_router.callback_query(F.data == "study_words")
async def study_words(
    callback: CallbackQuery,
    state: FSMContext,
):

    user_id = callback.from_user.id

    logger.info(
        "review_study_started user_id=%s",
        user_id,
    )

    await state.update_data(
        mode=MODE_REVIEW,
    )

    word = await learning_service.get_next_word(
        user_id=callback.from_user.id,
        mode=MODE_REVIEW,
    )

    if not word:
        logger.info(
            "review_study_finished_no_words user_id=%s",
            user_id,
        )

        await callback.message.answer(
            get_finish_message(MODE_REVIEW),
            reply_markup=back_menu_keyboard(),
        )

        await callback.answer()
        return

    # asyncpg.Record -> получаем id через ключ
    word_id = word["id"]

    logger.info(
        "review_study_word_selected user_id=%s word_id=%s",
        user_id,
        word_id,
    )

    audio_message_id = await send_study_word(
        callback.message,
        word,
        title=get_mode_title(MODE_REVIEW),
    )

    await state.update_data(
        audio_message_id=audio_message_id,
    )

    logger.info(
        "review_study_word_sent user_id=%s word_id=%s audio_message_id=%s",
        user_id,
        word_id,
        audio_message_id,
    )

    await callback.answer()


# =====================================
# Следующее слово
# =====================================

@review_router.callback_query(F.data == "next_review_word")
async def next_review_word(
    callback: CallbackQuery,
    state: FSMContext,
):
    user_id = callback.from_user.id

    data = await state.get_data()

    mode = data.get(
        "mode",
        MODE_REVIEW,
    )

    logger.info(
        "review_next_word_started user_id=%s mode=%s",
        user_id,
        mode,
    )

    word = await learning_service.get_next_word(
        user_id=callback.from_user.id,
        mode=mode,
    )

    if not word:
        logger.info(
            "review_finished_no_words user_id=%s mode=%s",
            user_id,
            mode,
        )

        await callback.message.answer(
            get_finish_message(mode),
            reply_markup=back_menu_keyboard(),
        )

        await state.clear()

        logger.info(
            "review_state_cleared user_id=%s mode=%s",
            user_id,
            mode,
        )

        await callback.answer()
        return

    # asyncpg.Record -> получаем id через ключ
    word_id = word["id"]

    logger.info(
        "review_next_word_selected user_id=%s mode=%s word_id=%s",
        user_id,
        mode,
        word_id,
    )

    audio_message_id = await send_study_word(
        callback.message,
        word,
        title=get_mode_title(mode),
    )

    await state.update_data(
        audio_message_id=audio_message_id,
    )

    logger.info(
        "review_next_word_sent user_id=%s mode=%s word_id=%s audio_message_id=%s",
        user_id,
        mode,
        word_id,
        audio_message_id,
    )

    await callback.answer()


# =====================================
# ЗНАЮ
# =====================================

@review_router.callback_query(F.data.startswith("word_known:"))
async def word_yes(
    callback: CallbackQuery,
    state: FSMContext,
):
    user_id = callback.from_user.id
    word_id = int(callback.data.split(":")[1])

    logger.info(
        "review_answer_received user_id=%s word_id=%s correct=%s",
        user_id,
        word_id,
        True,
    )

    await process_review_answer(
        callback=callback,
        state=state,
        word_id=word_id,
        correct=True,
    )


# =====================================
# НЕ ЗНАЮ
# =====================================

@review_router.callback_query(F.data.startswith("word_unknown:"))
async def word_no(
    callback: CallbackQuery,
    state: FSMContext,
):
    user_id = callback.from_user.id

    word_id = int(
        callback.data.split(":")[1]
    )

    logger.info(
        "review_answer_received user_id=%s word_id=%s correct=%s",
        user_id,
        word_id,
        False,
    )

    await process_review_answer(
        callback=callback,
        state=state,
        word_id=word_id,
        correct=False,
    )


# =====================================
# Обработка ответа
# =====================================

async def process_review_answer(
    callback: CallbackQuery,
    state: FSMContext,
    word_id: int,
    correct: bool,
):
    user_id = callback.from_user.id

    data = await state.get_data()

    mode = data.get(
        "mode",
        MODE_REVIEW,
    )

    audio_message_id = data.get(
        "audio_message_id",
    )

    logger.info(
        "review_answer_processing user_id=%s word_id=%s correct=%s mode=%s",
        user_id,
        word_id,
        correct,
        mode,
    )

    try:
        result = await learning_service.process_answer(
            user_id=callback.from_user.id,
            word_id=word_id,
            correct=correct,
            mode=mode,
            update_session=False,
        )

    except Exception:
        logger.exception(
            "review_answer_failed user_id=%s word_id=%s correct=%s mode=%s",
            user_id,
            word_id,
            correct,
            mode,
        )

        await callback.answer(
            "❌ Не удалось обработать ответ.",
            show_alert=True,
        )
        return

    logger.info(
        "review_answer_processed user_id=%s word_id=%s correct=%s finished=%s",
        user_id,
        word_id,
        correct,
        result.finished,
    )

    # =====================================
    # Удаляем сообщение со словом
    # Удаляем озвучку
    # =====================================

    await cleanup_word_message(
        message=callback.message,
        bot=callback.bot,
        audio_message_id=audio_message_id,
    )

    await asyncio.sleep(0.3)

    # =====================================
    # Показываем результат
    # =====================================

    if correct:
        result_message = await callback.message.answer(
            "✅ Правильно!\n"
            "⭐️ +5 XP"
        )
    else:
        result_message = await callback.message.answer(
            "📚 Повторим позже"
        )

    # Показываем результат короткое время
    await asyncio.sleep(0.5)

    try:
        await result_message.delete()
    except Exception:
        pass

    # =====================================
    # Обучение закончено
    # =====================================

    if result.finished:
        await callback.message.answer(
            get_finish_message(mode),
            reply_markup=back_menu_keyboard(),
        )

        await state.clear()

        await callback.answer()
        return

    # =====================================
    # Следующее слово
    # =====================================

    audio_message_id = await send_study_word(
        callback.message,
        result.next_word,
        title=get_mode_title(mode),
    )

    # =====================================
    # Сохраняем ID новой озвучки
    # =====================================

    await state.update_data(
        audio_message_id=audio_message_id,
    )

    await callback.answer()



