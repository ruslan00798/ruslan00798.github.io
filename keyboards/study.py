from aiogram.utils.keyboard import InlineKeyboardBuilder
from filters.history_data import LearnAnswerCallback

def new_answer_keyboard(
    answers,
    word_id: int,
):
    kb = InlineKeyboardBuilder()

    for answer in answers:
        kb.button(
            text=answer,
            callback_data=LearnAnswerCallback(
                word_id=word_id,
                answer=answer
            ).pack(),
        )

    kb.button(
        text="⏹ Завершить",
        callback_data="finish_learning",
    )

    kb.adjust(1)

    return kb.as_markup()    
           
