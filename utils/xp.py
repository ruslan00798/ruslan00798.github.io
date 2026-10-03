# utils/xp.py


# Награды за действия
XP_REWARDS: dict[str, int] = {
    # правильный ответ при обучении
    "study_correct": 10,
    # ежедневный вход
    "daily_login": 5,
}

STUDY_CORRECT_ACTION = "study_correct"
DAILY_LOGIN_ACTION = "daily_login"

SHORT_TRANSLATION_LENGTH = 10
XP_CHARS_PER_STEP = 20
MIN_TRANSLATION_XP = 2
MAX_TRANSLATION_XP = 20

def get_xp_reward(action: str) -> int:
    """
    Получить XP за действие
    """

    return XP_REWARDS.get(action, 0)


def calculate_study_xp(correct: bool) -> int:
    """
    XP за обучение слов.
    """

    if correct:

        return get_xp_reward(STUDY_CORRECT_ACTION)

    return 0

