from aiogram.filters.callback_data import CallbackData


class LearnCallback(CallbackData, prefix="learn"):
    id: int



class RepeatCallback(CallbackData, prefix="history_repeat"):
    id: int

class HistoryPageCallback(CallbackData, prefix="history_page"):
    page: int


class HistoryDeleteCallback(CallbackData, prefix="history_delete"):
    id: int

class FavoriteCallback(CallbackData, prefix="favorite"):
    id: int

class FavoriteRemoveCallback(CallbackData, prefix="favorite_remove"):
    id: int  

class VoiceHistoryCallback(CallbackData, prefix="voice_history"):
    id: int          

class LearnLevelCallback(CallbackData, prefix="learn_level"):
    level:str 

class LearnAnswerCallback(CallbackData, prefix="learn_answer"):
    word_id: int
    answer: str 

class LearnCategoryCallback(CallbackData, prefix="learn_category"):
    category: str

class VoiceCallback(CallbackData, prefix="voice"):
    word_id: int 

