# utils/xp.py


# Награды за действия
XP_REWARDS = {

    # обычный перевод текста
    "translation": 5,

    # перевод документа
    "document_translation": 15,

    # добавление в избранное
    "favorite": 2,

    # правильный ответ при обучении
    "study_correct": 10,

    # повторение сложного слова
    "study_repeat": 3,

    # ежедневный вход
    "daily_login": 5,

}



def get_xp_reward(
    action: str
) -> int:
    """
    Получить XP за действие
    """

    return XP_REWARDS.get(
        action,
        0
    )



def calculate_translation_xp(
    text: str
) -> int:
    """
    XP за перевод текста.

    Чем больше полезного текста —
    тем больше XP.
    """

    if not text:
        return 0


    length = len(
        text.strip()
    )


    # маленькие переводы
    if length < 10:
        return 1


    # обычный текст
    xp = length // 20


    # минимум 2 XP
    xp = max(
        xp,
        2
    )


    # максимум за один перевод
    xp = min(
        xp,
        20
    )


    return xp



def calculate_document_xp(
    characters: int
) -> int:
    """
    XP за перевод документа.
    """

    if characters <= 0:
        return 0


    xp = characters // 100


    return min(
        max(xp, 10),
        50
    )



def calculate_study_xp(
    correct: bool
) -> int:
    """
    XP за обучение слов.
    """

    if correct:

        return get_xp_reward(
            "study_correct"
        )


    return 0

def calculate_xp(
    text: str
) -> int:
    """
    Старое имя функции.
    Оставлено для совместимости
    с handlers.translate.py
    """

    return calculate_translation_xp(text)