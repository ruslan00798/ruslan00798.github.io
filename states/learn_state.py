from aiogram.fsm.state import State, StatesGroup


class LearnState(StatesGroup):
    choosing_level = State()
    waiting_word_answer = State()
    waiting_picture_answer = State()