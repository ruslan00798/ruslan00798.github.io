#======================
#ФАЙЛ learning_service.py ОТВЕЧАЕТ ЗА ПРАВИЛА И ОПЕРАЦИИ ОБУЧЕНИЯ
#ЭТО МОЗГ ОБУЧЕНИЯ ОТ ОТВЕЧАЕТ КАК ИМЕННО ЭТО СДЕЛАТЬ
#======================

from random import shuffle

from aiogram.fsm.context import FSMContext
from states.learn_state import LearnState

from database.requests import (
    add_word_progress,
    add_xp,
    get_language,
    get_learning_session,
    get_random_word,
    get_random_wrong_word,
    get_review_word,
    get_word_by_id,
    save_word_answer,
    update_session_result,
    get_random_picture_word,
    get_wrong_answers,
)

from services.dictionary_service import  get_or_create_word
from services.history_service import get_translation_history


async def prepare_picture_word(state: FSMContext) -> dict | None:
    """
    Получает слово с картинкой,
    сохраняет его в FSM.

    Возвращает слово,
    если оно найдено.
    """

    word = await get_random_picture_word()

    if not word:
        return None 
    
    await state.update_data(picture_word_id=word["id"])

    await state.set_state(LearnState.waiting_picture_answer)

    return word



# =====================
# Получение слов
# =====================

async def get_next_word(user_id: int, mode: str,) -> dict | None:
    """
    Возвращает следующее слово в зависимости от режима обучения
    Если подходящего слова нет возвращает None
    """

    language = await get_language(user_id)

    print("USER:", user_id)
    print("MODE:", mode)
    print("LANGUAGE:", language)

    if not language:
        return None
    
    if mode == "errors":
        return await get_random_wrong_word(user_id, language)
    
    if mode == "review":
        return await get_review_word(user_id, language)
    
    session = await get_learning_session(user_id)

    if not session:
        return None
    
    return await get_random_word(
        user_id,
        language,
        session["category"],
        session["level"],

    )


# =====================
# Сохранение результата
# =====================

async def save_word_result(
    user_id: int,
    word_id: int,
    correct: bool,
):
    """
    Сохраняет ответ пользователя
    и начисляет опыт.
    """

    await save_word_answer(
        user_id,
        word_id,
        correct,
    )

    await add_xp(
        user_id,
        5 if correct else 1,
    )


# =====================
# Сохранение результата
# Обновление сессии
# =====================

async def save_learning_result(
    user_id: int,
    word_id: int,
    correct: bool,
):
    """
    Сохраняет результат обучения
    и обновляет статистику сессии.
    """

    await save_word_result(
        user_id,
        word_id,
        correct,
    )

    await update_session_result(
        user_id,
        correct,
    )




# =====================
# Формирование текста
# =====================


def build_answer_text(correct: bool, translation: str,)->str:
    """
    Создаем сообщение после проверки ответа.
    """

    if correct:
        return(
            "✅ Правильно!\n"
            "⭐ +5 XP"
        )
    
    return(
        "❌ Неправильно!\n"
        f"Правильно: {translation}\n"
        "⭐ +1 XP"
    )

# =====================
# Формирование текста
# =====================


def get_finish_message(mode: str)->str:
    """
    Возвращает сообщение после окончания обучения.
    """

    if mode == "errors":
        return "Ошибок больше нет!"
    
    if mode == "review":
        return "🎉 Повторять пока нечего!"
    
    return "🎉 Все новые слова изучены!"

def get_mode_title(mode: str) -> str:
    """
    Возвращает заголовок для режима обучения.
    """

    if mode == "errors":
        return "🔁 Повторение ошибок"
    
    if mode == "review":
        return "📅 Повторение"
    
    return "🧠 Новое слово"


def build_picture_answer_text(correct: bool, word: str,) -> str:
    """
    Формирует сообщение после ответа
    в режиме картинок.
    """

    if correct:
        return(
            "✅ Правильно!\n"
            "⭐ +5 XP"
        )
    
    return (
        "❌ Неправильно.\n\n"
        f"Правильное слово: {word}"
    )

async def build_word_answers(word: dict):

    wrong = await get_wrong_answers(word["id"])

    answers = [word["translation"]]

    for item in wrong:
        answers.append(item["translation"])

    shuffle(answers)  

    return answers


def build_added_word_text(word: dict) -> str:
    """
    Формирует сообщение после добавления слова.
    """

    return (
        "🧠 <b>Новое слово</b>\n\n"
        f"🇬🇧 {word['word']}\n"
        f"🇷🇺 {word['translation']}\n\n"
        f"📚 Категория: {word['category']}\n"
        f"⭐ Уровень: {word['level']}\n\n"
        "✅ Слово добавлено в ваш словарь." 
    )


# =====================
# Проверка ответа
# =====================


def check_answer(user_answer: str, correct_answer: str,)-> bool:

    return user_answer.strip().lower() == correct_answer.strip().lower()

async def get_learning_word(word_id):
    return await get_word_by_id(word_id)





# =====================
# Добавляем слово из истории переводов
# =====================

async def add_word_from_history(user_id: int, history_id: int,):

    history = await get_translation_history (user_id, history_id)

    if history is None:
        return {
            "success": False,
            "error": "history_not_found"
        }
    
    word_id = await get_or_create_word(
        history["translated_text"],
        history["original_text"]
    )


    await add_word_progress(user_id, word_id)

    return {
        "success": True,
        "word": history["translated_text"],
        "translation": history["original_text"]
           
    }



    