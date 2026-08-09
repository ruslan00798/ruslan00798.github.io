from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def category_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🍎 Еда",
                    callback_data="category:food"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🐶 Животные",
                    callback_data="category:animals"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚗 Транспорт",
                    callback_data="category:transport"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Дом",
                    callback_data="category:home"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌎 Все слова",
                    callback_data="category:all"
                )
            ]
        ]
    )