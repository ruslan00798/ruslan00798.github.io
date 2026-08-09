from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def next_picture_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➡️ Следующее слово",
                    callback_data="next_picture"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 В меню",
                    callback_data="back_menu"
                )
            ]
        ]
    )