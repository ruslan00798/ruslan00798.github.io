from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def learn_mode_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🆕 Новые слова",
                    callback_data="mode:new"
                )
            ],

            [
                InlineKeyboardButton(
                    text="❌ Повторить ошибки",
                    callback_data="mode:errors"
                )
            ],

        ]
    )