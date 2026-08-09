from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def new_word_keyboard(word_id):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Знаю",
                    callback_data=f"word_yes:{word_id}"
                ),

                InlineKeyboardButton(
                    text="❌ Не знаю",
                    callback_data=f"word_no:{word_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="➡️ Следующее слово",
                    callback_data="learn_words"
                )
            ]
        ]
    )

def next_word_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➡️ Следующее слово",
                    callback_data="learn_words"
                )
            ]
        ]
    )