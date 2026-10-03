from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔤 Перевод текста", callback_data="translate_text")],
            [InlineKeyboardButton(text="📄 Перевод документа", callback_data="translate_document")],
            [InlineKeyboardButton(text="📚 История", callback_data="history")],
            [InlineKeyboardButton(text="⭐ Избранное", callback_data="favorites")],
            [InlineKeyboardButton(text="🌐 Выбрать язык", callback_data="settings")],
            
            [InlineKeyboardButton(text="🔁 Повторение", callback_data="study_words")],
            [InlineKeyboardButton(text="📚 Повторить ошибки", callback_data="repeat_errors")],
            [InlineKeyboardButton(text="📊 Прогресс", callback_data="study_progress")],
            
            [InlineKeyboardButton(text="🧠 Учить новые слова", callback_data="learn_words")],
            [InlineKeyboardButton(text="🖼️ - Картинка → слово. ", callback_data="picture_mode")],
            [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
            ]
    )
