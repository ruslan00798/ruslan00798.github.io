from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def favorites_keyboard(history_id: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🔊 Прослушать",
                    callback_data=f"voice:{history_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="❌ Убрать из избранного",
                    callback_data=f"favorite:{history_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🗑 Удалить",
                    callback_data=f"history_delete:{history_id}"
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