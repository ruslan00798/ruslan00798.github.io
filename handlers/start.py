#start.py
import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from services.daily_login_service import DailyLoginService
from keyboards.language_kbd import language_kbd
from keyboards.menu_kbd import main_menu
from services.learning.daily_repository import DailyLoginRepository

logger = logging.getLogger(__name__)

daily_login_repository = DailyLoginRepository()
daily_login_service = DailyLoginService(daily_login_repository)


start_router = Router()
   

@start_router.message(CommandStart())
async def start_cmd(message: Message):

    user_id = message.from_user.id

    logger.info(
        "start_command user_id=%s",
        user_id
    )

    try:

        language = await daily_login_service.get_language(user_id)

        logger.info(
        "start_user_status user_id=%s language=%s",
        user_id,
        language,
        )

        if language is None:

            await message.answer(
                "👋 Привет!\n\n"
                "Я бот-переводчик.\n"
                "Сначала выберите язык перевода:",
                reply_markup=language_kbd(),
            )
            return
        
        bonus = await daily_login_service.process_daily_login(user_id)

        logger.info(
        "daily_login_processed user_id=%s bonus=%s",
        user_id,
        bool(bonus),
        )

        bonus_text = ""

        if bonus:
            bonus_text = (
                "\n🔥 Новая серия дней!\n"
                f"🔥 Серия: {bonus['streak']} дней\n"
                f"⭐ +{bonus['xp']} XP за вход"
            )

        await message.answer(
            "👋 С возвращением!\n\n"
            "Выберите действие:"
            f"{bonus_text}",
            reply_markup=main_menu(),
        )

    except Exception:
        logger.exception(
            "start_command_failed user_id=%s",
            user_id,
        )

        await message.answer(
            "❌ Не удалось открыть главное меню." 
            "Попробуйте ещё раз."
        )
        raise    