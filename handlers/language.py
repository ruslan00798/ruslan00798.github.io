import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.menu_kbd import main_menu
from services.language_service import LanguageService
from services.learning.language_repository import LanguageRepository


language_router = Router()

language_repository = LanguageRepository()
language_service = LanguageService(language_repository)

logger = logging.getLogger(__name__)


LANGUAGES = {
    "en": "🇬🇧 English",
    "de": "🇩🇪 Deutsch",
    "ru": "🇷🇺 Русский",
    "ar": "🇸🇦 العربية",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
    "it": "🇮🇹 Italiano",
    "tr": "🇹🇷 Türkçe",
    "uk": "🇺🇦 Українська",
}


@language_router.callback_query(F.data.startswith("lang_"))
async def choose_language(callback: CallbackQuery) -> None:
    """
    Обрабатывает выбор языка перевода.
    """

    language_code = callback.data.removeprefix("lang_")
    user_id = callback.from_user.id

    logger.info(
        "language_selection_started user_id=%s language=%s",
        user_id,
        language_code,
    )

    if language_code not in LANGUAGES:
        logger.warning(
            "language_code_invalid user_id=%s language=%s",
            user_id,
            language_code,
        )

        await callback.answer(
            "❌ Неизвестный язык.",
            show_alert=True,
        )
        return

    await language_service.change_language(
        user_id=user_id,
        language_code=language_code,
    )

    logger.info(
        "language_changed user_id=%s language=%s",
        user_id,
        language_code,
    )

    await callback.message.edit_text(
        text=(
            "✅ Язык перевода установлен.\n\n"
            f"{LANGUAGES[language_code]}\n\n"
            "Теперь можно переводить."
        ),
        reply_markup=main_menu(),
    )

    await callback.answer()