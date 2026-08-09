from aiogram.filters.callback_data import CallbackData


class LearnCallback(
    CallbackData,
    prefix="learn"
):
    id: int



class RepeatCallback(
    CallbackData,
    prefix="repeat"
):
    id: int