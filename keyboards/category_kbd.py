from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.history_data import LearnCategoryCallback


def category_keyboard():

    kb = InlineKeyboardBuilder()

    kb.button(
        text="🍎 Еда",
        callback_data=LearnCategoryCallback(category="food").pack(),
    )

    kb.button(
          text="🐶 Животные",
          callback_data=LearnCategoryCallback(category="animals").pack(),
    )

    kb.button(
          text="🚗 Транспорт",
          callback_data=LearnCategoryCallback(category="transport").pack(),
    )

    kb.button(
          text="🏠 Дом",
          callback_data=LearnCategoryCallback(category="home").pack(),
    )

    kb.button(
           text="🌎 Все слова",
           callback_data=LearnCategoryCallback(category="all").pack(),
    )

    kb.adjust(1)

    return kb.as_markup()
       
           
          
    