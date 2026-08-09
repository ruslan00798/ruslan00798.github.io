from aiogram import Router, F

from aiogram.types import CallbackQuery


from database.requests import (
    get_statistics,
    get_xp,
    get_learned_words,
    get_language,
    get_daily_goal
)


from utils.level import calculate_level

from utils.achievements import get_achievements


from keyboards.back_menu_kbd import back_menu_keyboard



profile_router = Router()




@profile_router.callback_query(
    F.data == "profile"
)
async def profile(
    callback: CallbackQuery
):


    user_id = callback.from_user.id



    stats = await get_statistics(
        user_id
    )


    xp = await get_xp(
        user_id
    )


    learned = await get_learned_words(
        user_id
    )


    language = await get_language(
        user_id
    )


    goal = await get_daily_goal(
        user_id
    )



    level = calculate_level(
        xp
    )



    achievements = get_achievements(

        stats["translations"],

        xp,

        learned

    )



    if goal:


        progress = goal["completed"]

        target = goal["target"]


    else:


        progress = 0

        target = 10



    if target > 0:


        filled = int(
            progress / target * 10
        )


    else:


        filled = 0



    if filled > 10:

        filled = 10



    bar = (
        "█" * filled
        +
        "░" * (10 - filled)
    )



    text = (

        "👤 Профиль\n\n"


        f"🌐 Язык: "
        f"{language or 'не выбран'}\n\n"


        f"🏆 Уровень: "
        f"{level['level']}\n"


        f"⭐ XP: "
        f"{xp}\n"


        f"📈 До следующего уровня: "
        f"{level['need_xp'] - level['current_xp']} XP\n\n"



        f"📚 Переводов: "
        f"{stats['translations']}\n"


        f"⭐ Избранных: "
        f"{stats['favorites']}\n"


        f"🧠 Изучено слов: "
        f"{learned}\n\n"



        f"🎯 Цель дня:\n"

        f"{bar} {progress}/{target}\n\n"



        "🏅 Достижения:\n"

        +

        "\n".join(
            achievements[:5]
        )

    )



    await callback.message.edit_text(

        text,

        reply_markup=back_menu_keyboard()

    )



    await callback.answer()