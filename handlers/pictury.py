import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from keyboards.picture_kbd import next_picture_keyboard
from services.learning.repository import LearningRepository
from services.learning_service import LearningService
from services.word_sender import build_picture_answer_text
from states.learn_state import LearnState


learning_repository = LearningRepository()
learning_service = LearningService(learning_repository)

picture_router = Router()

logger = logging.getLogger(__name__)


@picture_router.callback_query(F.data == "picture_mode")
async def picture_mode_start(
    callback: CallbackQuery,
    state: FSMContext,
):
    user_id = callback.from_user.id

    logger.info(
        "Пользователь запускает picture mode: user_id=%s",
        user_id,
    )

    try:
        word = await learning_service.prepare_picture_word()

        if not word:
            logger.warning(
                "Не найдено слов с картинками: user_id=%s",
                user_id,
            )

            await callback.message.answer(
                "❌ Нет слов с картинками"
            )

            await callback.answer()
            return

        logger.info(
            "Получено слово для picture mode: user_id=%s word_id=%s",
            user_id,
            word["id"],
        )

        await state.update_data(
            picture_word_id=word["id"]
        )

        await state.set_state(
            LearnState.waiting_picture_answer
        )

        await callback.message.answer_photo(
            photo=word["image_url"],
            caption="🖼️ Что изображено?\nНапишите слово:",
        )

        logger.info(
            "Картинка отправлена пользователю: user_id=%s word_id=%s",
            user_id,
            word["id"],
        )

        await callback.answer()

    except Exception:
        logger.exception(
            "Ошибка при запуске picture mode: user_id=%s",
            user_id,
        )

        await callback.message.answer(
            "❌ Произошла ошибка. Попробуйте ещё раз."
        )

        await callback.answer()


@picture_router.message(LearnState.waiting_picture_answer)
async def check_picture_answer(
    message: Message,
    state: FSMContext,
):
    user_id = message.from_user.id

    logger.info(
        "Получен ответ в picture mode: user_id=%s",
        user_id,
    )

    if not message.text:
        logger.warning(
            "Пользователь отправил сообщение без текста: user_id=%s",
            user_id,
        )

        await message.answer(
            "✍️ Напишите слово текстом."
        )
        return

    data = await state.get_data()

    word_id = data.get("picture_word_id")

    logger.debug(
        "Получены данные FSM: user_id=%s word_id=%s",
        user_id,
        word_id,
    )

    if not word_id:
        logger.warning(
            "В FSM отсутствует picture_word_id: user_id=%s",
            user_id,
        )

        await message.answer(
            "Ошибка. Начните заново."
        )

        await state.clear()
        return

    try:
        word, correct = await learning_service.process_picture_answer(
            user_id=user_id,
            word_id=word_id,
            answer=message.text,
        )

        if word is None:
            logger.warning(
                "Слово не найдено при проверке ответа: "
                "user_id=%s word_id=%s",
                user_id,
                word_id,
            )

            await message.answer(
                "Слово не найдено."
            )

            await state.clear()
            return

        logger.info(
            "Ответ проверен: user_id=%s word_id=%s correct=%s",
            user_id,
            word_id,
            correct,
        )

        await message.answer(
            build_picture_answer_text(
                correct=correct,
                word=word["word"],
            ),
            reply_markup=next_picture_keyboard(),
        )

        await state.clear()

        logger.debug(
            "FSM очищен после проверки ответа: user_id=%s",
            user_id,
        )

    except Exception:
        logger.exception(
            "Ошибка при проверке ответа: user_id=%s word_id=%s",
            user_id,
            word_id,
        )

        await message.answer(
            "❌ Произошла ошибка при проверке ответа."
        )

        await state.clear()


@picture_router.callback_query(F.data == "next_picture")
async def next_picture(
    callback: CallbackQuery,
    state: FSMContext,
):
    user_id = callback.from_user.id

    logger.info(
        "Пользователь запросил следующую картинку: user_id=%s",
        user_id,
    )

    try:
        word = await learning_service.prepare_picture_word()

        if not word:
            logger.warning(
                "Не найдено следующего слова с картинкой: user_id=%s",
                user_id,
            )

            await callback.message.answer(
                "❌ Нет слов с картинками"
            )

            await callback.answer()
            return

        logger.info(
            "Получено следующее слово: user_id=%s word_id=%s",
            user_id,
            word["id"],
        )

        await state.update_data(
            picture_word_id=word["id"]
        )

        await state.set_state(
            LearnState.waiting_picture_answer
        )

        await callback.message.answer_photo(
            photo=word["image_url"],
            caption="🖼️ Что изображено?\nНапишите слово:",
        )

        logger.info(
            "Следующая картинка отправлена: user_id=%s word_id=%s",
            user_id,
            word["id"],
        )

        await callback.answer()

    except Exception:
        logger.exception(
            "Ошибка при получении следующей картинки: user_id=%s",
            user_id,
        )

        await callback.message.answer(
            "❌ Произошла ошибка. Попробуйте ещё раз."
        )

        await callback.answer()
