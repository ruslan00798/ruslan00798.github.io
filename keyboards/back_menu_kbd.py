from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def back_menu_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏠 В меню",
                    callback_data="back_menu"
                )
            ]
        ]
    )