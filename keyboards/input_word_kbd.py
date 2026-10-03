from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.history_data import InputWordCallback, SkipWordCallback, VoiceCallback


def input_word_keyboard(word_id: int):

    kb = InlineKeyboardBuilder()

    kb.button(
        text="🔊 Произнести",
        callback_data=VoiceCallback(
            word_id=word_id
        ).pack(),
    )

    kb.adjust(1)

    return kb.as_markup()