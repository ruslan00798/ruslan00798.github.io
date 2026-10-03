from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def language_kbd():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇬🇧 English",
                    callback_data="lang_en"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇩🇪 Deutsch",
                    callback_data="lang_de"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇷🇺 Русский",
                    callback_data="lang_ru"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇸🇦 العربية",
                    callback_data="lang_ar"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇫🇷 Français",
                    callback_data="lang_fr"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇪🇸 Español",
                    callback_data="lang_es"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇮🇹 Italiano",
                    callback_data="lang_it"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇹🇷 Türkçe",
                    callback_data="lang_tr"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇺🇦 Українська",
                    callback_data="lang_uk"
                )
            ],
        ]
    )

    return keyboard
