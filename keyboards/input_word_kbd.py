from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def input_word_keyboard(word_id: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✍️ Ввести ответ",
                    callback_data=f"input_word:{word_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔊 Произнести",
                    callback_data=f"voice:{word_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⏭ Пропустить",
                    callback_data="skip_word"
                )
            ]
        ]
    )