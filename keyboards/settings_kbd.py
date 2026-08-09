from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def settings_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌐 Выбрать язык",
                    callback_data="change_language"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="back_menu"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔊 Автоозвучка",
                    callback_data="voice_settings"
                )
            ]
        ]
    )