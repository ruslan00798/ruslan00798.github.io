#learn.py

import asyncio
import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from filters.history_data import (
    LearnAnswerCallback,
    LearnLevelCallback,
    LearnCategoryCallback
)
from keyboards.back_menu_kbd import back_menu_keyboard
from keyboards.category_kbd import category_keyboard
from keyboards.level_kbd import level_keyboard
from services.learning.constants import MODE_NEW
from services.learning.repository import LearningRepository
from services.learning_service import LearningService
from services.message_service import cleanup_word_message
from services.word_sender import (
    build_answer_text,
    get_finish_message,
    get_mode_title,
    send_word,
)
from states.learn_state import LearnState

logger = logging.getLogger(__name__)

learning_repository = LearningRepository()
learning_service = LearningService(learning_repository)


learn_router = Router()


@learn_router.callback_query(F.data == "learn_words")
async def learn_words(callback: CallbackQuery):

    logger.info(
        "User %s opened learning menu",
        callback.from_user.id
    )

    await callback.message.answer(
        "📚 Выберите категорию:",
        reply_markup=category_keyboard()
    )

    await callback.answer()


@learn_router.callback_query(LearnCategoryCallback.filter())
async def select_category(callback: CallbackQuery, state: FSMContext, callback_data: LearnCategoryCallback):

    category = callback_data.category

    logger.info(
        "User %s selected category=%s",
        callback.from_user.id,
        category
    )

    await state.update_data(category=category)

    await state.set_state(LearnState.choosing_level)

    await callback.message.edit_text(
        f"📂 Категория: {category}\n\n"
        "🎓 Выберите уровень:",
        reply_markup=level_keyboard()
    )


    await callback.answer()


@learn_router.callback_query(LearnState.choosing_level, LearnLevelCallback.filter())
async def select_level(
    callback: CallbackQuery, 
    state: FSMContext, 
    callback_data: LearnLevelCallback
):

    data = await state.get_data()

    category = data["category"]

    level = callback_data.level

    logger.info(
        "User %s selected level=%s for category=%s",
        callback.from_user.id,
        level,
        category
    )

    result = await learning_service.start_new_learning(
        user_id=callback.from_user.id,
        category=category,
        level=level
    )

    if not result:

        await callback.message.answer(
            "😔 Для этого уровня пока нет слов."
        )

        await state.clear()
        await callback.answer()

        return
    
    await state.update_data(
        mode=result["mode"],
        level=level
    )

    await callback.message.delete()

    audio_message_id = await send_word(
        callback.message,
        result["word"],
        title="🧠 Новое слово"
    )

    await state.update_data(
        audio_message_id=audio_message_id,
    )

    await callback.answer()


@learn_router.callback_query(LearnAnswerCallback.filter())
async def learn_answer(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: LearnAnswerCallback,
):

    word_id = callback_data.word_id
    answer = callback_data.answer

    data = await state.get_data()

    mode = data.get("mode", MODE_NEW)
    audio_message_id = data.get("audio_message_id")

    result = await learning_service.process_answer(
        user_id=callback.from_user.id,
        word_id=word_id,
        answer=answer,
        mode=mode,
        update_session=True,
    )

     
    if result.word is None:
        await callback.message.answer(
            "❌ Слово не найдено."
        )

        await callback.answer()
        return
   
    await  cleanup_word_message(
        message=callback.message,
        bot=callback.bot,
        audio_message_id=audio_message_id
    )

    await asyncio.sleep(0.3)
    

    # =====================================
    # Показываем результат
    # =====================================

    result_message = await callback.message.answer(
        build_answer_text(
            correct=result.correct,
            translation=result.word["translation"],
        )
    )

    # Результат показываем 1 секунды
    await asyncio.sleep(1.0)

    try:
        await result_message.delete()
    except TelegramBadRequest:
        # Сообщение уже могло быть удалено.
        pass

    if result.finished:

        await callback.message.answer(
            get_finish_message(mode),
            reply_markup=back_menu_keyboard(),
        )

        await state.clear()

        await callback.answer()
        return

    audio_message_id = await send_word(
        callback.message,
        result.next_word,
        title=get_mode_title(mode),
    )
    
    await state.update_data(
        audio_message_id=audio_message_id,
    )

    await callback.answer()

# =====================================
# Завершение обучения
# =====================================

@learn_router.callback_query(F.data == "finish_learning")
async def finish_learning_handler(
    callback: CallbackQuery
):

    result = await learning_service.finish_learning(
        user_id=callback.from_user.id
    )

    if not result:
        await callback.message.answer(
            "Сессия ещё не начата."
        )
        await callback.answer()
        return

    await callback.message.answer(
        "🎉 Обучение завершено!\n\n"
        f"📚 Всего ответов: {result['total_answers']}\n"
        f"✅ Правильно: {result['correct_answers']}\n"
        f"❌ Ошибки: {result['wrong_answers']}",
        reply_markup=back_menu_keyboard()
    )

    await callback.answer()

