from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def study_keyboard(word_id: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Знаю",
                    callback_data=f"word_known:{word_id}"
                ),

                InlineKeyboardButton(
                    text="❌ Не знаю",
                    callback_data=f"word_unknown:{word_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⏭ Следующее",
                    callback_data="next_review_word"
                )
            ]
        ]
    )