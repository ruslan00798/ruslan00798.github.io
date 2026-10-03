from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.history_data import (
    FavoriteRemoveCallback,
    HistoryDeleteCallback,
)


def favorites_keyboard(history_id: int):

    kb = InlineKeyboardBuilder()


    kb.button(
        text="🔊 Прослушать",
        callback_data=f"voice_history:{history_id}"
    )


    kb.button(
        text="❌ Убрать из избранного",
        callback_data=FavoriteRemoveCallback(id=history_id).pack()
    )


    kb.button(
        text="🗑 Удалить",
        callback_data=HistoryDeleteCallback(id=history_id).pack()
    )


    kb.button(
        text="🏠 В меню",
        callback_data="back_menu"
    )


    kb.adjust(1)
        


    return kb.as_markup()


