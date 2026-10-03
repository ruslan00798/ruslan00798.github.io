#history.py
import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from filters.history_data import (
    FavoriteCallback,
    FavoriteRemoveCallback,
    HistoryDeleteCallback,
    HistoryPageCallback,
    LearnCallback,
)

from keyboards.back_menu_kbd import back_menu_keyboard
from keyboards.favorites_kbd import favorites_keyboard
from keyboards.history_kbd import (
    history_item_keyboard,
    history_navigation_keyboard,
)

from services.dictionary_service import DictionaryService
from services.history_service import HistoryService
from services.learning.dictionary_repository import DictionaryRepository
from services.learning.history_repository import HistoryRepository
from services.message_service import get_error_message

history_repository = HistoryRepository()
history_service = HistoryService(history_repository)

dictionary_repository = DictionaryRepository()
dictionary_service = DictionaryService(dictionary_repository, history_service)

history_router = Router()
logger = logging.getLogger(__name__)


# =========================
# История
# =========================

async def send_history(
    message: Message,
    user_id: int,
    page: int = 0,
) -> None:
    history, has_next = await history_service.get_history_page(
        user_id,
        page,
    )

    if not history:
        await message.answer(
            "📚 История переводов пуста.",
            reply_markup=back_menu_keyboard(),
        )
        return

    for item in history:
        await message.answer(
            f"🕒 {item['created_at']:%d.%m.%Y %H:%M}\n"
            f"📝 {item['original_text']}\n"
            f"➡️ {item['translated_text']}",
            reply_markup=history_item_keyboard(item["id"]),
        )

    await message.answer(
        "📚 Навигация:",
        reply_markup=history_navigation_keyboard(
            page=page,
            has_next=has_next,
        ),
    )


@history_router.callback_query(F.data == "history")
async def history_button(callback: CallbackQuery):

    logger.info(
        "history_opened user_id=%s page=%s",
        callback.from_user.id,
    )

    await send_history(callback.message, callback.from_user.id,)

    await callback.answer()


@history_router.callback_query(HistoryPageCallback.filter())
async def history_page(
    callback: CallbackQuery,
    callback_data: HistoryPageCallback,
):
    page = max(0, callback_data.page)

    logger.info(
        "history_page_opened user_id=%s page=%s",
        callback.from_user.id,
        page,
    )

    await callback.message.delete()

    await send_history(
        callback.message,
        callback.from_user.id,
        page,
    )

    await callback.answer()


@history_router.callback_query(F.data == "history_clear")
async def history_clear(callback: CallbackQuery):

    logger.info(
        "history_clear_started user_id=%s",
        callback.from_user.id,
    )

    await history_service.clear_user_history(callback.from_user.id,)

    await callback.message.edit_text(
        "🗑 История переводов очищена.",
        reply_markup=back_menu_keyboard(),
    )

    logger.info(
        "history_cleared user_id=%s",
        callback.from_user.id,
    )
     
    await callback.answer()


@history_router.callback_query(HistoryDeleteCallback.filter())
async def history_delete(
    callback: CallbackQuery,
    callback_data: HistoryDeleteCallback,
):

    logger.info(
        "history_delete_started user_id=%s history_id=%s",
        callback.from_user.id,
        callback_data.id,
    )

    deleted = await history_service.delete_user_history_item(
        callback.from_user.id,
        callback_data.id,
    )

    if deleted:
        logger.info(
            "history_deleted user_id=%s history_id=%s",
            callback.from_user.id,
            callback_data.id,
        )

        await callback.message.edit_text(
            "🗑 Перевод удалён."
        )

        await callback.answer()
        return
    
    logger.warning(
        "history_delete_not_found user_id=%s history_id=%s",
        callback.from_user.id,
        callback_data.id,
    )  

    await callback.answer(
        "❌ Перевод не найден.",
        show_alert=True,
    )


@history_router.callback_query(F.data == "favorites")
async def favorites(callback: CallbackQuery):

    logger.info(
        "favorite_opened user_id=%s",
        callback.from_user.id,
    )

    favorites = await history_service.get_user_favorites(
        callback.from_user.id,
    )

    if not favorites:
        logger.warning(
            "favorites_empty user_id=%s",
            callback.from_user.id,
        )

        await callback.message.answer(
            "⭐ Избранных переводов нет.",
            reply_markup=back_menu_keyboard(),
        )
        await callback.answer()
        return

    for row in favorites:
        await callback.message.answer(
            f"📝 {row['original_text']}\n"
            f"➡️ {row['translated_text']}",
            reply_markup=favorites_keyboard(row["id"]),
        )

    await callback.answer()


@history_router.callback_query(FavoriteCallback.filter())
async def favorite_button(
    callback: CallbackQuery,
    callback_data: FavoriteCallback,
):

    logger.info(
        "favorite_toggle user_id=%s history_id=%s",
        callback.from_user.id,
        callback_data.id,
    )

    result = await history_service.toggle_user_favorite(
        callback.from_user.id,
        callback_data.id,
    )

    if result:
        await callback.answer(
            "⭐ Добавлено в избранное"
        )
    else:
        await callback.answer(
            "❌ Убрано из избранного"
        )


@history_router.callback_query(FavoriteRemoveCallback.filter())
async def favorite_remove_button(
    callback: CallbackQuery,
    callback_data: FavoriteRemoveCallback,
):
    logger.info(
        "favorite_remove_started user_id=%s history_id=%s",
        callback.from_user.id,
        callback_data.id,
    )
    result = await history_service.remove_user_favorite(
        callback.from_user.id,
        callback_data.id,
    )

    if result is not None:
        logger.info(
            "favorite_remove_not_found user_id=%s history_id=%s",
            callback.from_user.id,
            callback_data.id,
        )

        await callback.answer(
            "❌ Убрано из избранного"
        )
        return
    
    logger.warning(
    "favorite_remove_not_found user_id=%s history_id=%s",
    callback.from_user.id,
    callback_data.id,
    )

    await callback.answer(
        "❌ Перевод не найден.",
        show_alert=True,
    )


# =========================
# Обучение
# =========================

@history_router.callback_query(LearnCallback.filter())
async def learn_word(
    callback: CallbackQuery,
    callback_data: LearnCallback,
):
    logger.info(
        "learn_word_started user_id=%s history_id=%s",
        callback.from_user.id,
        callback_data.id,
    )

    result = await dictionary_service.add_word_from_history(
        callback.from_user.id,
        callback_data.id,
    )

    if not result["success"]:
        logger.warning(
            "learn_word_not_found user_id=%s history_id=%s error=%s",
            callback.from_user.id,
            callback_data.id,
            result["error"],
        )
        await callback.answer(
            get_error_message(result["error"]),
            show_alert=True,
        )
        return
    logger.info(
        "learn_word_added user_id=%s history_id=%s word=%s",
        callback.from_user.id,
        callback_data.id,
        result["word"],
    )

    await callback.message.answer(
        "🧠 Слово добавлено!\n\n"
        f"🇬🇧 {result['word']}\n"
        f"🇷🇺 {result['translation']}"
    )

    await callback.answer()
