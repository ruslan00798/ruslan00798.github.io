import os

from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from callbacks.callback_data import (
    LearnCallback,
    RepeatCallback
)

from database.requests import (
    get_history_by_id,
    get_statistics,
    get_language,
    toggle_favorite,
    get_study_progress,
    get_learned_words,
)

from keyboards.back_menu_kbd import back_menu_keyboard

from services.learning_service import add_word_from_history
from services.message_service import get_error_message
from services.tts import text_to_speech
from services.profile_service import get_user_xp

from utils.level import calculate_level
from utils.achievements import get_achievements





callbacks_router = Router()



# =========================
# XP
# =========================


@callbacks_router.callback_query( F.data == "xp") 

async def show_xp(callback: CallbackQuery): 
    
    
    xp = await get_user_xp(callback.from_user.id)
    
    
    await callback.message.answer(f"⭐ Твой XP: {xp}")
    
    await callback.answer()
    

# =========================
# Учить слово.    В ЭТОМ ОБРАБОТЧИКЕ ОШИБКА
# =========================

@callbacks_router.callback_query(LearnCallback.filter())
async def learn_word(
    callback: CallbackQuery,
    callback_data: LearnCallback
):

    result = await add_word_from_history(
        callback.from_user.id,
        callback_data.id
    )


    if not result["success"]:

        await callback.answer(
            get_error_message(result["error"]),
            show_alert=True
        )

        return
    
    await callback.message.answer(
        "🧠 Слово добавлено!\n\n"
        f"🇬🇧 {result['word']}\n"
        f"🇷🇺 {result['translation']}"
    )

    await callback.answer()



  
# =========================
# Повторить
# =========================

# 🔁 Повторить перевод
@callbacks_router.callback_query(RepeatCallback.filter())#при нажатиии кнопки повторить декоратор вызывает функцию repeat_word
async def repeat_word(callback: CallbackQuery,callback_data: RepeatCallback):
    #получаем перевод из истории
    history = await get_history_by_id(callback.from_user.id,callback_data.id)

    #ЕСЛИ ПЕРЕВОД НЕ НАЙДЕН ВЫПОЛНЯЕТСЯ ЭТО УСЛОВИЕ
    if history is None:

        await callback.answer(
            "❌ Перевод не найден.",
            show_alert=True
        )

        return


    #ПОКАЗЫВАЕТ ПЕРЕВОД ПОЛЬЗОВАТЕЛЮ
    await callback.message.answer(
        "🔁 Повтори перевод:\n\n"
        f"🌍 {history['original_text']}\n\n"
        f"➡️ {history['translated_text']}"
    )

     #ЗАВЕРШАЕМ ОБРАБОТКИ КНОПКИ
    await callback.answer()
    

# =========================
# Озвучка
# =========================

@callbacks_router.callback_query(F.data.startswith("voice:")) #обраотчик кнопки "Прослушать"
async def voice(callback: CallbackQuery):#Она будет вызвана автоматически после нажатия кнопки

    history_id = int(callback.data.split(":")[1]) #получаем ID перевода.Допустим Telegram прислал:callback.data = "voice:25"
    #split(":") разделяет строку по символу получится список:["voice","25"] [1]-берет второй элемент списка получится 25

    #Получаем перевод из истории
    history = await get_history_by_id(
        callback.from_user.id,
        history_id
    )

    #Если перевод не найден выполняется это условие
    if not history:

        await callback.answer(
            "❌ Перевод не найден.",
            show_alert=True
        )

        return


    #Получаем выбранный язык пользователя  например: "en", "fr"
    language = await get_language(
        callback.from_user.id
    )

    #Проверяем язык пользователя если язык не выбран выполняется это условие 
    if not language:

        await callback.answer(
            "❌ Язык не выбран.",
            show_alert=True
        )

        return
    

    audio_path = None 

    try:
        #1)Создание аудио
        audio_path = await text_to_speech(
            history["translated_text"], 
        )
       

       
        await callback.message.answer_voice(
            
            FSInputFile(audio_path)
        )

    ############## Блок except
    #Если внутри  try произощла ошибка выполнение программы переходит сюда
    
    except Exception as error:
        

        await callback.answer(
            "❌ Ошибка озвучки.",
            show_alert=True
        )


    finally:

        if (
            audio_path
            and
            os.path.exists(audio_path) 
        ):

            os.remove(
                audio_path
            ) 


    await callback.answer()



# =========================
# Избранное
# =========================

@callbacks_router.callback_query(F.data.startswith("favorite:"))
async def favorite(callback: CallbackQuery):

    history_id = int(callback.data.split(":")[1])


    result = await toggle_favorite(
        callback.from_user.id,
        history_id
    )


    if result:

        await callback.answer(
            "⭐ Добавлено в избранное"
        )

    else:

        await callback.answer(
            "❌ Убрано из избранного"
        )

# =========================
# Статистика
# =========================

@callbacks_router.callback_query(F.data == "statistics")
async def statistics(callback: CallbackQuery):

    stats = await get_statistics(callback.from_user.id) #получаем статистику из базы данных


    xp = await get_user_xp(callback.from_user.id)  #получаем xp из базы данных


    level = calculate_level(xp) 
    

    await callback.message.answer( #дальше отправляем сообщение 
        "📊 Ваша статистика\n\n"
        f"🏆 Уровень: {level['level']}\n"
        f"⭐ XP: {xp}\n\n"
        f"🌍 Переводов: {stats['translations']}\n"
        f"❤️ Избранных: {stats['favorites']}"
    )
   
    await callback.answer()



# =========================
# Прогресс обучения
# =========================

@callbacks_router.callback_query(F.data == "study_progress")
async def study_progress(callback: CallbackQuery):

    progress = await get_study_progress(callback.from_user.id)


    await callback.message.answer(
        "📊 Прогресс обучения\n\n"
        f"📝 Всего слов: {progress['total_words']}\n"
        f"✅ Выучено: {progress['learned_words']}\n"
        f"❌ Сложные слова: {progress['difficult_words']}",
        reply_markup=back_menu_keyboard()
    )


    await callback.answer()



# =========================
# Достижения
# =========================

@callbacks_router.callback_query(F.data == "achievements")
async def achievements(callback: CallbackQuery):

    stats = await get_statistics(callback.from_user.id) 
    

    xp = await get_user_xp(callback.from_user.id) 
    

    learned = await get_learned_words(callback.from_user.id) #ПОЛУЧАЕМ КОЛИЧЕСТВО ИЗУЧЕННЫХ СЛОВ
    

    result = get_achievements( 
        stats["translations"],
        xp,
        learned
    )


    await callback.message.answer(
        "🏅 Достижения\n\n"
        + #обычное сложение строк
        "\n".join(result), #метод join все элементы списка через символ новой строки
        reply_markup=back_menu_keyboard()
    )


    await callback.answer()

    