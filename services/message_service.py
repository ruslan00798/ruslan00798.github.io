ERROR_MESSAGES = {
    "history_not_found":
        "❌ Перевод не найден.",

     "word_not_found":
        "❌ Слово не найдено в словаре.",    
}


def get_error_message(error: str) -> str:

    return ERROR_MESSAGES.get(error, "❌ Неизвестная ошибка.")