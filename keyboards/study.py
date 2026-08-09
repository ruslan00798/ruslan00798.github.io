from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def new_answer_keyboard(
    answers,
    word_id
):

    buttons = []


    for answer in answers:

        buttons.append(
            [
                InlineKeyboardButton(
                    text=answer,
                    callback_data=f"learn_answer:{word_id}:{answer}"
                )
            ]
        )


    buttons.append(
        [
            InlineKeyboardButton(
                text="🔊 Прослушать",
                callback_data=f"voice:{word_id}"
            )
        ]
    )


    buttons.append(
        [
            InlineKeyboardButton(
                text="⏹ Завершить",
                callback_data="finish_learning"
            )
        ]
    )


    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

def answer_keyboard(
    answers,
    word_id
):

    buttons = []


    for answer in answers:

        buttons.append(
            [
                InlineKeyboardButton(
                    text=answer,
                    callback_data=f"answer:{word_id}:{answer}"
                )
            ]
        )


    buttons.append(
        [
            InlineKeyboardButton(
                text="🔊 Прослушать",
                callback_data=f"voice:{word_id}"
            )
        ]
    )


    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )