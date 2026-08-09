from aiogram import Router, F
from aiogram.types import CallbackQuery


from database.requests import (
    update_language,
    update_daily_goal
)


from keyboards.menu_kbd import main_menu


language_router = Router()



LANGUAGES = {

    "en": "🇬🇧 English",

    "de": "🇩🇪 Deutsch",

    "ru": "🇷🇺 Русский",

    "ar": "🇸🇦 العربية"

}




@language_router.callback_query(F.data.startswith("lang_"))
async def choose_language(callback: CallbackQuery) -> None:
    """
    Обрабатывает выбор языка перевода.
    """

    language_code = callback.data.removeprefix("lang_")



    if language_code not in LANGUAGES:

        await callback.answer(

            "❌ Неизвестный язык.",

            show_alert=True

        )

        return



    user_id = callback.from_user.id

    await update_language(user_id, language_code)
    await update_daily_goal(user_id)

    await callback.message.edit_text(
        text=(
             "✅ Язык перевода установлен.\n\n"
            f"{LANGUAGES[language_code]}\n\n"
            "Теперь можно переводить."
        ),
        reply_markup=main_menu()
    )
    await callback.answer