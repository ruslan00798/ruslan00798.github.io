from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.requests import get_word_by_id
from keyboards.picture_kbd import next_picture_keyboard
from services.learning_service import build_picture_answer_text, prepare_picture_word, save_word_result
from states.learn_state import LearnState

picture_router = Router()




@picture_router.callback_query(F.data == "picture_mode")
async def picture_mode_start(callback: CallbackQuery,state: FSMContext):

    word = await prepare_picture_word(state)

    if not word:
        await callback.message.answer( "❌ Нет слов с картинками")

        await callback.answer()
        return
    
    await callback.message.answer_photo(
        photo=word["image_url"],
        caption="🖼️ Что изображено?\nНапишите слово:"
    )

    await callback.answer()





@picture_router.message(LearnState.waiting_picture_answer)
async def check_picture_answer(message: Message,state: FSMContext):

    if not message.text:
        await message.answer(
            "✍️ Напишите слово текстом."
        )
        return

   
    data = await state.get_data()
   

    word_id = data.get("picture_word_id")


    if not word_id:
        await message.answer(
            "Ошибка. Начните заново."
        )
        await state.clear()
        return


    word = await get_word_by_id(word_id)


    if not word:
        await message.answer(
            "Слово не найдено."
        )
        await state.clear()
        return

    user_answer = (message.text.strip().lower())


    correct = (user_answer ==  word["word"].strip().lower())
        
    
    await save_word_result(
        user_id=message.from_user.id,
        word_id=word_id,
        correct=correct,
    )

    await message.answer(
    build_picture_answer_text(
        correct=correct,
        word=word["word"],
    ),
    reply_markup=next_picture_keyboard(),
)

    
    await state.clear()





@picture_router.callback_query(F.data == "next_picture")
async def next_picture(callback: CallbackQuery,state: FSMContext):

    word = await prepare_picture_word(state)

    if not word:
        await callback.message.answer("❌ Нет слов с картинками")

        await callback.answer()

        return
    
    await callback.message.answer_photo(
        photo=word["image_url"],
        caption="🖼️ Что изображено?\nНапишите слово:"
    )

    await callback.answer()