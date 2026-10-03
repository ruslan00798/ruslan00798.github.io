#profile.py
import logging
from aiogram import Router, F

from aiogram.types import CallbackQuery

from keyboards.back_menu_kbd import back_menu_keyboard
from services.learning.profile_repository import ProfileRepository
from services.profile_service import ProfileService 

profile_repository = ProfileRepository()
profile_sevice = ProfileService(profile_repository)

profile_router = Router()

logger = logging.getLogger(__name__)


@profile_router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):

    logger.info(
        "profile_opened user_id=%s",
        callback.from_user.id,
    )

    data = await profile_sevice.get_profile_data(callback.from_user.id)


    await callback.message.edit_text(
            profile_sevice.build_profile_text(data),
            reply_markup=back_menu_keyboard()
        )


    await callback.answer()
    

    


# =========================
# Достижения
# =========================

@profile_router.callback_query(F.data == "achievements")
async def achievements(callback: CallbackQuery):

    logger.info(
        "achievements_opened user_id=%s",
        callback.from_user.id,
    )

    text = await profile_sevice.get_achievements_text(callback.from_user.id)

    await callback.message.edit_text(
        text,
        reply_markup=back_menu_keyboard()
    )

    await callback.answer()

# =========================
# Прогресс обучения
# =========================

@profile_router.callback_query(F.data == "study_progress")
async def study_progress(callback: CallbackQuery):

   logger.info(
       "study_progress_opened user_id=%s",
       callback.from_user.id,
   )

   text = await profile_sevice.get_study_progress_text(callback.from_user.id)

   await callback.message.edit_text(
       text,
       reply_markup=back_menu_keyboard()
    )

   await callback.answer()