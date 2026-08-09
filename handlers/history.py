from aiogram import Router, F

from aiogram.filters import Command

from aiogram.types import Message, CallbackQuery

from database.requests import (
    get_history,
    clear_history,
    delete_history,
    get_history_by_id,
    get_favorites
)


from keyboards.back_menu_kbd import back_menu_keyboard
from keyboards.menu_kbd import main_menu
from keyboards.history_kbd import history_keyboard
from keyboards.favorites_kbd import favorites_keyboard



history_router = Router()

PAGE_SIZE = 5


async def build_history_text(user_id: int, page: int):
    """
    Получает историю переводов и формирует текст сообщения.
    """

    history = await get_history(
       user_id=user_id,
       limit=PAGE_SIZE,
       offset=page * PAGE_SIZE, 
    )

    if not history:
        return None, None
    
    #список строк будущего сообщения
    lines = ["📚 Последние переводы:\n"]

    for row in history:
       lines.append(
           (
            f"🕒 {row['created_at']:%d.%m.%Y %H:%M}\n"
            f"📝{row['original_text']}"
            f"➡️{row['translated_text']}\n\n"
        )
    )
       #обеденяем все строки  в один текст
       text = "\n".join(lines)
    return text, history[-1]["id"]

#Отправляет историю пользователю
async def send_history(message: Message, user_id: int, page: int = 0,):
    text, last_id = await build_history_text(user_id, page)

    if text is None:
        await message.answer(
            "📚 История переводов пуста.",
            reply_markup=main_menu(),
        )
        return
    
    await message.answer(
        text,
        reply_markup=history_keyboard(last_id,page,)
    )

@history_router.message(Command("history"))
async def history_command(message: Message):

    await send_history(message, message.from_user.id)


@history_router.callback_query(F.data == "history")
async def history_button(callback: CallbackQuery):

    await send_history(callback.message, callback.from_user.id)

    await callback.answer()

#Пагинация страниц истории
@history_router.callback_query(F.data.startswith("history_page:"))
async def history_page(callback: CallbackQuery):

    page = max(0, int(callback.data.split(":")[1]))
    
    await callback.message.delete()

    await send_history(callback.message, callback.from_user.id, page,)

    await callback.answer()

#Удаление истории
@history_router.callback_query(F.data == "history_clear") 
async def history_clear(callback: CallbackQuery):

    await clear_history(callback.from_user.id)

    await callback.message.edit_text(
          "🗑 История переводов очищена.",
          reply_markup=back_menu_keyboard(),
    )
    await callback.answer()

#Удаление одного перевода
@history_router.callback_query(F.data.startswith("history_delete"))
async def history_delete(callback: CallbackQuery):

    history_id = int(callback.data.split(":")[1])

    await delete_history(callback.from_user.id, history_id,)

    await callback.message.edit_text("🗑 Перевод удалён.")

    await callback.answer()


#Повтор перевода
@history_router.callback_query(F.data.startswith("history_repeat:"))
async def history_repeat(callback: CallbackQuery):

    history_id = int(callback.data.split(":")[1])

    row = await get_history_by_id(callback.from_user.id, history_id)

    if row is None:

        await callback.answer(
            "❌ Перевод не найден.",
            show_alert=True,
        )
        return
    
    await callback.message.answer(
        "🔁 Повтор перевода:\n\n"
        f"📝 {row['original_text']}\n\n"
        f"➡️ {row['translated_text']}"
    )
    await callback.answer()


#Избранное
@history_router.callback_query(F.data == "favorites")
async def favorites(callback: CallbackQuery):

    favorites = await get_favorites(callback.from_user.id)

    if not favorites:
        await callback.message.answer(
            "⭐ Избранных переводов нет.",
            reply_markup=back_menu_keyboard(),
        )

        await callback.answer()
        return
    
    for row in favorites:
        await callback.message.answer(
            f"📝{row['original_text']}\n"
            f"➡️{row['translated_text']}",
            reply_markup=favorites_keyboard(row["id"])
        )

    await callback.answer()

"""
    Пользователь
      |
      |
  /history
      |
      ↓
history_command()
      |
      ↓
send_history()
      |
      ↓
build_history_text()
      |
      ↓
get_history()
      |
      ↓
База данных
      |
      ↓
Текст + кнопки
      |
      ↓
Telegram
    """    
