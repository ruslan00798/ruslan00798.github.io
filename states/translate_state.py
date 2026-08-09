from aiogram.fsm.state import (
    StatesGroup,
    State
)


class TranslateState(
    StatesGroup
):
    """
    Состояния пользователя
    во время перевода.
    """

    # Пользователь должен отправить текст
    waiting_text = State()


    # Пользователь должен отправить файл
    waiting_document = State()