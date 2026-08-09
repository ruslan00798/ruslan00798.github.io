from aiogram.utils.keyboard import InlineKeyboardBuilder


def history_keyboard(
    history_id: int,
    page: int = 0
):

    kb = InlineKeyboardBuilder()

    kb.button(
        text="🔄 Повторить",
        callback_data=f"history_repeat:{history_id}"
    )




    kb.button(
        text="🗑 Удалить",
        callback_data=f"history_delete:{history_id}"
    )


    kb.button(
        text="⬅️",
        callback_data=f"history_page:{page-1}"
    )


    kb.button(
        text="➡️",
        callback_data=f"history_page:{page+1}"
    )


    kb.button(
        text="🗑 Очистить всю историю",
        callback_data="history_clear"
    )


    kb.adjust(
        1,
        2,
        1
    )


    return kb.as_markup()