from aiogram import Router, F

from aiogram.types import CallbackQuery


from database.requests import toggle_voice_setting
from keyboards.settings_kbd import settings_menu

from keyboards.language_kbd import language_kbd



settings_router = Router()




# ==========================
# Настройки
# ==========================

@settings_router.callback_query(
    F.data == "settings"
)
async def settings(
    callback: CallbackQuery
):


    await callback.message.edit_text(

        "⚙️ Настройки:",

        reply_markup=settings_menu()

    )



    await callback.answer()




# ==========================
# Изменить язык
# ==========================

@settings_router.callback_query(
    F.data == "change_language"
)
async def change_language(
    callback: CallbackQuery
):


    await callback.message.edit_text(

        "🌐 Выберите язык перевода:",

        reply_markup=language_kbd()

    )



    await callback.answer()

@settings_router.callback_query(
    F.data == "voice_settings"
)
async def voice_settings(
    callback: CallbackQuery
):

    user_id = callback.from_user.id


    status = await toggle_voice_setting(
        user_id
    )


    text = (
        "🔊 Автоозвучка включена"
        if status
        else
        "🔇 Автоозвучка выключена"
    )


    await callback.message.answer(
        text
    )


    await callback.answer()    