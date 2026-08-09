from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def level_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟢 A1",
                    callback_data="level:A1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔵 A2",
                    callback_data="level:A2"
                )
            ],
              [
                InlineKeyboardButton(
                    text="🟡 B1",
                    callback_data="level:B1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟠 B2",
                    callback_data="level:B2"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔴 C1",
                    callback_data="level:C1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚫ C2",
                    callback_data="level:C2"
                )
            ]

        ]
    )