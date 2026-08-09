from aiogram import Router, F
from aiogram.types import CallbackQuery
from random import shuffle


from database.requests import (
    get_review_count,
    get_word_for_review,
    get_language,
   
    get_word_by_id,
    save_word_answer,
    add_xp,
)



from keyboards.back_menu_kbd import back_menu_keyboard
from aiogram.fsm.context import FSMContext
from services.word_sender import send_study_word, send_word



study_router = Router()



# ==========================
# Начать повторение
# ==========================

@study_router.callback_query(F.data == "study_words")
async def study_words(
    callback: CallbackQuery,
    state: FSMContext
):

    user_id = callback.from_user.id


    await state.update_data(
        mode="review"
    )


    language = await get_language(
        user_id
    )


    if not language:

        await callback.message.answer(
            "❗ Сначала выберите язык."
        )

        await callback.answer()

        return



    count = await get_review_count(
        user_id
    )


    if count == 0:

        await callback.message.answer(
            "🎉 Отлично!\n\n"
            "Сегодня нет слов для повторения.",
            reply_markup=back_menu_keyboard()
        )

        await callback.answer()

        return



    word = await get_word_for_review(
        user_id,
        language
    )


    if not word:

        await callback.message.answer(
            "🎉 Нет слов для повторения.",
            reply_markup=back_menu_keyboard()
        )

        await callback.answer()

        return



    await send_study_word(
        callback,
        word,
        title="🔁 Повторение"
    )


    await callback.answer()


# ==========================
# Ответ
# ==========================

@study_router.callback_query(
    F.data.startswith("answer:")
)
async def answer(callback: CallbackQuery):


    await callback.answer()


    user_id = callback.from_user.id


    _, word_id, selected = callback.data.split(
        ":",
        2
    )


    word_id = int(word_id)



    word = await get_word_by_id(
        word_id
    )


    if not word:

        await callback.message.answer(
            "❌ Слово не найдено."
        )

        return



    correct = (
        selected == word["translation"]
    )



    await save_word_answer(
        user_id,
        word_id,
        correct
    )



    await add_xp(
        user_id,
        5 if correct else 1
    )



    if correct:

        await callback.message.answer(
            "✅ Правильно!\n⭐ +5 XP"
        )

    else:

        await callback.message.answer(
            "❌ Ошибка\n\n"
            f"Правильно: {word['translation']}\n"
            "⭐ +1 XP"
        )



    language = await get_language(
        user_id
    )


    next_word = await get_word_for_review(
        user_id,
        language
    )



    if not next_word:


        await callback.message.answer(
            "🎉 Повторение закончено!",
            reply_markup=back_menu_keyboard()
        )

        return



    await send_word(
        callback,
        next_word,
        title="🔁 Повторение"
    )