from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.history_data  import LearnLevelCallback


def level_keyboard():

    kb = InlineKeyboardBuilder()


    kb.button(
        text="🟢 A1",
        callback_data=LearnLevelCallback(level="A1").pack()
    )

    kb.button(
       text= "🔵 A2",
       callback_data=LearnLevelCallback(level="A2").pack() 
    )

    kb.button(
        text="🟡 B1",
        callback_data=LearnLevelCallback(level="B1").pack()

    )

    kb.button(
        text="🟠 B2",
        callback_data=LearnLevelCallback(level="B2").pack()

    ) 

    kb.button(
        text="🔴 C1",
        callback_data=LearnLevelCallback(level="C1").pack()
    )

    kb.button(
        text="⚫ C2",
        callback_data=LearnLevelCallback(level="C2").pack()
    )

    kb.adjust(1)


    return kb.as_markup()

       
       
            
           
             
           
            
            
           