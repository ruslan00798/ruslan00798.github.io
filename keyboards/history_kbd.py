from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.history_data import (
    HistoryDeleteCallback,
    HistoryPageCallback,
    RepeatCallback
)



def history_item_keyboard(history_id: int):

    kb = InlineKeyboardBuilder()

    kb.button(
        text="🔄 Повторить",
        callback_data=RepeatCallback(id=history_id).pack()
    )

    delete_callback = HistoryDeleteCallback(
        id=history_id
    ).pack()

    kb.button(
        text="🗑 Удалить",
        callback_data=delete_callback,
    )

    kb.adjust(2)

    return kb.as_markup()



def history_navigation_keyboard(
    page: int,
    has_next: bool,
):
    kb = InlineKeyboardBuilder()

    if page > 0:
        previous_callback = HistoryPageCallback(page=page - 1).pack()

        kb.button(
            text="⬅️",
            callback_data=previous_callback,
        )

    if has_next:
        next_callback = HistoryPageCallback(page=page + 1).pack()

        kb.button(
            text="➡️",
            callback_data=next_callback,
        )

    kb.button(
        text="🗑 Очистить всю историю",
        callback_data="history_clear",
    )

    if page > 0 and has_next:
        kb.adjust(2, 1)
    else:
        kb.adjust(1, 1)

    return kb.as_markup()
