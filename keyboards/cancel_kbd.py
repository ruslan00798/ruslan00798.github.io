from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def cancel_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data="cancel"
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