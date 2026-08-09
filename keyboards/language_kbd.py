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
        ]
    ]   
)
    return keyboard