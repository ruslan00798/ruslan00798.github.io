from random import shuffle

from aiogram.types import Message

from keyboards.study import new_answer_keyboard
from keyboards.study_kbd import study_keyboard
from database.requests import get_wrong_answers
from services.voice_service import send_word_voice

from models.translation import TranslationError


# =========================================================
# Новое слово
# =========================================================

async def send_word(
    message: Message,
    word: dict,
    title: str = "🧠 Новое слово",
):
    """
    Отправляет новое слово и его озвучку.

    Возвращает message_id сообщения с озвучкой.
    """

    answers = await build_word_answers(word)

    text = (
        f"{title}\n\n"
        f"🇬🇧 {word['word']}\n\n"
        "Выберите перевод:"
    )

    keyboard = new_answer_keyboard(
        answers,
        word["id"],
    )

    # -----------------------------------------------------
    # Отправляем слово
    # -----------------------------------------------------

    if word.get("image_url"):

        try:

            await message.answer_photo(
                photo=word["image_url"],
                caption=text,
                reply_markup=keyboard,
            )

        except Exception:

            await message.answer(
                text,
                reply_markup=keyboard,
            )

    else:

        await message.answer(
            text,
            reply_markup=keyboard,
        )

    # -----------------------------------------------------
    # Автоматическая озвучка
    # -----------------------------------------------------

    audio_message_id = await send_word_voice(
        message=message,
        word=word,
    )

    return audio_message_id


# =========================================================
# Повторение слова
# =========================================================

async def send_study_word(
    message: Message,
    word: dict,
    title: str = "🔁 Повторение",
):
    """
    Отправляет слово для повторения
    и его озвучку.

    Возвращает message_id сообщения с озвучкой.
    """

    text = (
        f"{title}\n\n"
        f"🇬🇧 {word['word']}\n\n"
        "Вы знаете это слово?"
    )

    await message.answer(
        text,
        reply_markup=study_keyboard(
            word["id"]
        ),
    )

    audio_message_id = await send_word_voice(
        message=message,
        word=word,
    )

    return audio_message_id


# =========================================================
# Формирование текста ответа
# =========================================================

def build_answer_text(
    correct: bool,
    translation: str,
) -> str:
    """
    Создает сообщение после проверки ответа.
    """

    if correct:

        return (
            "✅ Правильно!\n"
            "⭐ +5 XP"
        )

    return (
        "❌ Неправильно!\n"
        f"Правильно: {translation}\n"
        "⭐ +1 XP"
    )


# =========================================================
# Сообщение окончания обучения
# =========================================================

def get_finish_message(
    mode: str,
) -> str:

    if mode == "errors":

        return "🎉 Ошибок больше нет!"

    if mode == "review":

        return "🎉 Повторять пока нечего!"

    return "🎉 Все новые слова изучены!"


# =========================================================
# Заголовок режима
# =========================================================

def get_mode_title(
    mode: str,
) -> str:

    if mode == "errors":

        return "🔁 Повторение ошибок"

    if mode == "review":

        return "📅 Повторение"

    return "🧠 Новое слово"


# =========================================================
# Ответ в режиме картинок
# =========================================================

def build_picture_answer_text(
    correct: bool,
    word: str,
) -> str:

    if correct:

        return (
            "✅ Правильно!\n"
            "⭐ +5 XP"
        )

    return (
        "❌ Неправильно.\n\n"
        f"Правильное слово: {word}"
    )


# =========================================================
# Варианты переводов
# =========================================================

async def build_word_answers(
    word: dict,
):

    wrong = await get_wrong_answers(
        word["id"]
    )

    answers = [
        word["translation"]
    ]

    for item in wrong:

        answers.append(
            item["translation"]
        )

    shuffle(answers)

    return answers


async def handle_translation_error(message: Message, error: TranslationError | None ) -> None:

    if error == TranslationError.LANGUAGE_NOT_SELECTED:
        await message.answer( "❗ Сначала выберите язык перевода.")
        return

    if error == TranslationError.EMPTY_TEXT:
        await message.answer( "❌ Текст не может быть пустым.")
        return
    await message.answer( "❌ Не удалось получить перевод. Попробуйте позже.")