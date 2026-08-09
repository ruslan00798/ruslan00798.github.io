from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.requests import (
    add_xp,
    get_language,
    update_daily_goal,
    update_streak
)

from keyboards.language_kbd import language_kbd
from keyboards.menu_kbd import main_menu

start_router = Router()

async def get_bonus_text(user_id: int) -> str:
    """
    Обновляет ежедневную серию и возвращает текст бонуса.
    """

    streak, is_new_day = await update_streak(user_id)

    await update_daily_goal(user_id)

    if not is_new_day:
        return ""
    await add_xp(user_id, 5)

    return(
        "\n🔥 Новая серия дней!\n"
        f"🔥 Серия: {streak} дней\n"
        "⭐ +5 XP за вход"
    )

@start_router.message(CommandStart())
async def start_cmd(message: Message):

    user_id = message.from_user.id

    language = await get_language(user_id)

    if language is None:

        await message.answer(
            "👋 Привет!\n\n"
            "Я бот-переводчик.\n"
            "Сначала выберите язык перевода:",
            reply_markup=language_kbd(),
        )
        return
    
    bonus_text = await get_bonus_text(user_id)

    await message.answer(
        "👋 С возвращением!\n\n"
        "Выберите действие:"
        f"{bonus_text}",
        reply_markup=main_menu(),
    )