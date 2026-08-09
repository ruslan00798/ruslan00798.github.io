import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import (
    FSInputFile,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)




from database.requests import (
    get_language,
    save_history,
    add_xp,
    get_history_by_id,
    get_word
)


from services.translator import (
    translate,
    add_harakat_simple
)


from services.tts import get_voice, text_to_speech
from states.translate_state import TranslateState
from utils.xp import calculate_xp


from callbacks.callback_data import (
    RepeatCallback,
    LearnCallback
)



translate_router = Router()



# ==========================
# Общая обработка перевода
# ==========================

async def process_translation(message: Message, text: str, user_id: int):


    language = await get_language(user_id)


    if not language:

        await message.answer("❗ Сначала выберите язык перевода.")

        return



    db_word = await get_word(text)

    if db_word:
        translated = db_word["translation"]
    else:
        translated = await translate(
            text,
            language
        )


    if language == "ar":

        translated = add_harakat_simple(
            translated
        )



    xp = calculate_xp(
        text
    )


    await add_xp(
        user_id,
        xp
    )



    history_id = await save_history(
        user_id,
        text,
        translated
    )



    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🧠 Учить",
                    callback_data=LearnCallback(
                        id=history_id
                    ).pack()
                )
            ],


            [
                InlineKeyboardButton(
                    text="🔁 Повторить",
                    callback_data=RepeatCallback(
                        id=history_id
                    ).pack()
                )
            ],


            [
                InlineKeyboardButton(
                    text="🔊 Прослушать",
                    callback_data=f"voice_history:{history_id}"
                )
            ],


            [
                InlineKeyboardButton(
                    text="⭐ В избранное",
                    callback_data=f"voice_history:{history_id}"
                )
            ],


            [
                InlineKeyboardButton(
                    text="⭐ Мой XP",
                    callback_data="xp"
                )
            ],


            [
                InlineKeyboardButton(
                    text="🏠 В меню",
                    callback_data="back_menu"
                )
            ]

        ]
    )



    await message.answer(
        "🌍 Перевод:\n\n"
        f"{translated}\n\n"
        f"⭐ +{xp} XP",
        reply_markup=keyboard
    )




# ==========================
# Перевод текста
# ==========================



@translate_router.message(TranslateState.waiting_text,F.text)
async def translate_text(message: Message):

    text = message.text.strip()


    if len(text) > 5000:

        await message.answer(
            "❌ Максимальная длина текста — 5000 символов."
        )
        return


    try:

        await process_translation(
            message,
            text,
            message.from_user.id
        )


    except Exception as error:

        print(
            "ОШИБКА ПЕРЕВОДА:",
            repr(error)
        )

        await message.answer(
            "❌ Ошибка перевода."
        )
# ==========================
# Повторить перевод
# ==========================

@translate_router.callback_query(
    RepeatCallback.filter()
)
async def repeat_translation(
    callback: CallbackQuery,
    callback_data: RepeatCallback
):


    history = await get_history_by_id(
        callback.from_user.id,
        callback_data.id
    )



    if not history:


        await callback.answer(
            "❌ Перевод не найден.",
            show_alert=True
        )

        return



    await process_translation(
        callback.message,
        history["original_text"],
        callback.from_user.id
    )



    await callback.answer()

@translate_router.callback_query(
    F.data.startswith("voice_history:")
)
async def play_translation_voice(
        callback: CallbackQuery
):

    await callback.answer()


    history_id = int(
        callback.data.split(":")[1]
    )


    history = await get_history_by_id(
        callback.from_user.id,
        history_id
    )


    if not history:
        await callback.message.answer(
            "❌ Перевод не найден"
        )
        return


    text = history["translated_text"]


    language = await get_language(
        callback.from_user.id
    )


    file_path = await text_to_speech(
        text,
        get_voice(language)
    )


    await callback.message.answer_audio(
        audio=FSInputFile(file_path),
        caption=f"🔊 {text}"
    )


    os.remove(file_path)