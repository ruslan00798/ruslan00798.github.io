from aiogram import Router, F

from aiogram.types import CallbackQuery #Тип объекта, приходящего при нажатии inline-кнопки

from aiogram.fsm.context import FSMContext #Контекст машины состояния пользователя
"""
#FSM-это машинное состояние (FINITE STATE MACHINE)
она хранит "что сейчас делает пользователь"
Например:

ожидаем имя
|
ожидаем возраст
|
ожидаем телефон
FSMContext позволяет 

1.сохранить данные
(await state.update_data(...))

2.получить данные
await state.get_data(...)

3.изменить состояние
await state.set_state(...)

4.удалить состояние
await state.clear(...)
"""
from keyboards.menu_kbd import main_menu #Функция создания клавиатуры главного меню



cancel_router = Router() #Router обработчика в него будут добовлятся обработчики отмены




@cancel_router.callback_query(F.data == "cancel") #Обработчик нажатия кнопки отмены
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    """
    Очистка состояния (await state.clear()) самая важная строка 
    она полностью очищает 

    состояние, данные, FSM
    например:

    До 

    State = WaitingName

    data

    {
      "name": "Иван"
    } 

    после 

    State = None
    data = {} то есть бот забывает что он что то вводил
    """
    


    await callback.message.edit_text(
        #метод edit_text не отправляет новое сообщение а изменяет уже существующее
        #например до "введите имя", после "действие отменено, главное меню" преимущество чат остаётся чистым
        "✅ Действие отменено.\n\n"

        "Главное меню:",

        reply_markup=main_menu()

    )



    await callback.answer()

"""
Как читается весь код по порядку

    1.Импортируются необходимые классы и функции.

    2.Создается роутер cancel_router.

    3.Регистрируется обработчик для callback-кнопки с data == "cancel".

    4.Пользователь нажимает кнопку «Отмена».

    5.Telegram отправляет CallbackQuery.

    6.Вызывается функция cancel_action().

    7.Выполняется state.clear(), полностью сбрасывая текщее FSM-состояние и связанные с ним данные.

    8.Текст текущего сообщения изменяется на «Действие отменено».

    9.Вместо старой клавиатуры прикрепляется главное меню (main_menu()).

    10.Выполняется callback.answer(), чтобы Telegram завершил обработку нажатия кнопки.
"""    