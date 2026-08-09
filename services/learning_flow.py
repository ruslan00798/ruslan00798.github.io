# ======================
# ФАЙЛ learning_flow.py ОТВЕЧАЕТ ЗА ПОРЯДОК ДЕЙТСВИЙ
# УПРАВЛЯЕТ ПРОЦЕССОМ
# ======================


from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from services.learning_service import (
    build_answer_text,
    check_answer,
    get_learning_word,
    get_next_word,
    get_finish_message,
    get_mode_title,
    save_learning_result,
    save_word_result,
)

from services.word_sender import (
    send_word,
    send_study_word,
)

from keyboards.back_menu_kbd import back_menu_keyboard

# =========================
# Запуск режима обучения
# =========================


async def get_mode_word(
    state: FSMContext,
    user_id: int,
    mode: str,
):
    

    await state.update_data(mode=mode)

    word = await get_next_word(
        user_id=user_id,
        mode=mode,
    )

    return word


async def start_review_mode(
    callback: CallbackQuery,
    state: FSMContext,
    mode: str,
):

    word = await get_mode_word(state=state, user_id=callback.from_user.id, mode=mode)

    if not word:

        await callback.message.answer(
            get_finish_message(mode),
            reply_markup=back_menu_keyboard(),
        )
        return

    await send_study_word(callback, word, title=get_mode_title(mode))


# =========================
# Отправка следующего слова
# =========================
async def send_next_word(
    callback: CallbackQuery,
    state: FSMContext
):

    user_id = callback.from_user.id

    data = await state.get_data()

    mode = data.get("mode", "new")

    word = await get_next_word(
        user_id=user_id,
        mode=mode
    )


    if not word:

        await callback.message.answer(
            get_finish_message(mode),
            reply_markup=back_menu_keyboard(),
        )

        await state.clear()

        return


    if mode in ("review", "errors"):

        await send_study_word(
            callback,
            word,
            title=get_mode_title(mode)
        )

    else:

        await send_word(
            callback,
            word,
            title=get_mode_title(mode)
        )

# =========================
# Обработка ответов
# =========================
async def process_word_answer(
    callback: CallbackQuery, state: FSMContext, word_id: int, correct: bool
):
    
    print("WORD ANSWER")
    print("WORD ID:", word_id)
    print("CORRECT:", correct)


    await save_word_result(
        user_id=callback.from_user.id,
        word_id=word_id,
        correct=correct,
    ) 

    if correct:
        await callback.answer("✅ +5 XP")
    else:
        await callback.answer("📚 Повторим позже")

    await send_next_word(callback, state)


# =========================
# Ответы пользователя
# =========================
async def process_learning_answer(callback: CallbackQuery, state: FSMContext):

    user_id = callback.from_user.id

    _, word_id, answer = callback.data.split(":", 2)

    word_id = int(word_id)

    word = await get_learning_word(word_id)

    if not word:
        await callback.message.answer("❌ Слово не найдено.")

        return

    correct = check_answer(answer, word["translation"])

    await save_learning_result(user_id=user_id, word_id=word_id, correct=correct)

    await callback.message.answer(
        build_answer_text(correct=correct, translation=word["translation"])
    )

    await send_next_word(callback, state)