from aiogram.utils.keyboard import InlineKeyboardBuilder
from filters.history_data import (
    RepeatCallback, 
    LearnCallback, 
    FavoriteCallback,
    VoiceHistoryCallback
)    




def translate_keyboard(history_id: int):

    kb = InlineKeyboardBuilder()

    kb.button(
        text="🧠 Учить",
        callback_data=LearnCallback(id=history_id).pack()
    )

    kb.button(
        text="🔄 Повторить",
        callback_data=RepeatCallback(id=history_id).pack()
    )

    kb.button(
        text="🔊 Прослушать",
        callback_data=VoiceHistoryCallback(id=history_id).pack()
    )

    kb.button(
        text="⭐ В избранное",
        callback_data=FavoriteCallback(id=history_id).pack()
    )

    kb.button(
        text="🏠 В меню",
        callback_data="back_menu"
    )

    kb.adjust(1)

    return kb.as_markup()