#result.py

from dataclasses import dataclass

@dataclass
class LearningResult:
    """
    Результат ответа пользователя на слово
    """

    correct: bool
    next_word: dict | None
    finished: bool
    word: dict | None