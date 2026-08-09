import os
from random import shuffle

from services.learning_service import  build_word_answers
from keyboards.study import new_answer_keyboard
from keyboards.study_kbd import study_keyboard
from services.voice_service import send_word_voice

from aiogram.types import CallbackQuery, FSInputFile



async def send_word(callback: CallbackQuery, word, title="🧠 Новое слово"):
    print("SEND NORMAL WORD") 
    answers = await build_word_answers(word)

    text = (
        f"{title}\n\n"
        f"🇬🇧 {word['word']}\n\n"
        "Выберите перевод:"
    )


    if word.get("image_url"):


        try:

            await callback.message.answer_photo(
                photo=word["image_url"],
                caption=text,
                reply_markup=new_answer_keyboard(
                    answers,
                    word["id"]
                )
            )

        except Exception as error:


           

            await callback.message.answer(
                text,
                reply_markup=new_answer_keyboard(
                    answers,
                    word["id"]
                )
            )



    else:


        await callback.message.answer(
            text,
            reply_markup=new_answer_keyboard(
                answers,
                word["id"]
            )
        )

    # ==========================
    # Озвучка
    # ==========================

    await send_word_voice(callback, word)


async def send_study_word(callback: CallbackQuery, word: dict, title= "🔁 Повторение"):
    print("SEND STUDY WORD")
    text = (
        f"{title}\n\n"
        f"🇬🇧 {word['word']}\n\n"
        "Вы знаете это слово?"
    )

    await callback.message.answer(
        text,
        reply_markup=study_keyboard(
            word["id"]
        )
    )