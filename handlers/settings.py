#settings.py
import logging
from aiogram import Router, F

from aiogram.types import CallbackQuery
from keyboards.settings_kbd import settings_menu
from keyboards.language_kbd import language_kbd

settings_router = Router()

logger = logging.getLogger(__name__)

@settings_router.callback_query(F.data == "settings")
async def settings(callback: CallbackQuery):

    logger.info(
        "settings opened user_id=%s",
        callback.from_user.id,
    )
    
    await callback.message.edit_text(
        "⚙️ Настройки:",
        reply_markup=settings_menu()
    )

    await callback.answer()

@settings_router.callback_query(F.data == "change_language")
async def change_language(callback: CallbackQuery):

    logger.info(
        "change_language_opened user_id=%s",
        callback.from_user.id,
    )

    await callback.message.edit_text(
        "🌐 Выберите язык перевода:",
        reply_markup=language_kbd()
    )

    await callback.answer()

