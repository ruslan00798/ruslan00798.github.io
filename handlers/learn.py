#Сторонние библиотеки
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


#Локальные модули проекта
from database.requests import (
    finish_session,
    get_language,
    save_learning_session,
    get_random_word,
    add_word_progress,
    
)

from states.learn_state import LearnState
from services.learning_flow import  process_learning_answer, process_word_answer
from services.word_sender import send_word
from keyboards.back_menu_kbd import back_menu_keyboard
from keyboards.category_kbd import category_keyboard
from keyboards.level_kbd import level_keyboard



learn_router = Router()


# ====================================
# Новые слова
# =====================================

@learn_router.callback_query(F.data == "learn_words")
async def learn_words(callback: CallbackQuery):

    await callback.message.answer(
        "📚 Выберите категорию:",
        reply_markup=category_keyboard()
    )

    await callback.answer()



# =====================================
# Выбор категории
# =====================================

@learn_router.callback_query(F.data.startswith("category:"))
async def select_category(
    callback: CallbackQuery,
    state: FSMContext
):

    category = callback.data.split(":")[1]


    await state.update_data(
        category=category
    )


    await state.set_state(
        LearnState.choosing_level
    )


    await callback.message.answer(
        f"📂 Категория: {category}\n\n"
        "🎓 Выберите уровень:",
        reply_markup=level_keyboard()
    )


    await callback.answer()



# =====================================
# Выбор уровня
# =====================================

@learn_router.callback_query(LearnState.choosing_level, F.data.startswith("level:"))
async def select_level(callback: CallbackQuery,state: FSMContext):

    user_id = callback.from_user.id


    language = await get_language(
        user_id
    )


    data = await state.get_data()


    category = data["category"]


    level = callback.data.split(":")[1]



    await save_learning_session(
        user_id,
        category,
        level
    )


    # сохраняем режим!
    await state.update_data(
        mode="new",
        category=category,
        level=level
    )



    word = await get_random_word(
        user_id,
        language,
        category,
        level
    )



    if not word:

        await callback.message.answer(
            "😔 Для этого уровня пока нет слов."
        )

        await state.clear()

        await callback.answer()

        return
    

    await add_word_progress(user_id, word["id"])



    await send_word(
        callback,
        word,
        title="🧠 Новое слово"
    )


    await callback.answer()





# =====================================
# Ответы пользователя
# =====================================


@learn_router.callback_query(F.data.startswith("learn_answer:"))
async def learn_answer(callback: CallbackQuery,state: FSMContext):

    await process_learning_answer(
        callback,
        state,
    )

    



#ЗНАЮ
@learn_router.callback_query(F.data.startswith("word_known:"))
async def word_yes(callback: CallbackQuery, state: FSMContext):

    word_id = int(callback.data.split(":")[1])

    await process_word_answer(
        callback=callback,
        state=state,
        word_id=word_id,
        correct=True,
    )
  


#НЕ ЗНАЮ
@learn_router.callback_query(F.data.startswith("word_unknown:"))
async def word_no(callback: CallbackQuery, state: FSMContext):

    word_id = int(callback.data.split(":")[1])

    await process_word_answer(
        callback=callback,
        state=state,
        word_id=word_id,
        correct=False,
    )

# =====================================
# Завершение обучения
# =====================================

@learn_router.callback_query(F.data == "finish_learning")
async def finish_learning( callback: CallbackQuery):

    user_id = callback.from_user.id

    result = await finish_session(
        user_id
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

@learn_router.callback_query(F.data.startswith("input_word:"))
async def input_word_start(callback: CallbackQuery,state: FSMContext):

    word_id = int(callback.data.split(":")[1])


    await state.update_data(input_word_id=word_id)


    await state.set_state(LearnState.waiting_word_answer)


    await callback.message.answer("✍️ Напишите перевод слова:")


    await callback.answer()


