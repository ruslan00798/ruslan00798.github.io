#cansel.py

from aiogram import Router, F

from aiogram.types import CallbackQuery #Тип объекта, приходящего при нажатии inline-кнопки

from aiogram.fsm.context import FSMContext #Контекст машины состояния пользователя

from keyboards.menu_kbd import main_menu #Функция создания клавиатуры главного меню



cancel_router = Router() #Router обработчика в него будут добовлятся обработчики отмены




@cancel_router.callback_query(F.data == "cancel") #Обработчик нажатия кнопки отмены
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    


    await callback.message.edit_text(
        #метод edit_text не отправляет новое сообщение а изменяет уже существующее
        #например до "введите имя", после "действие отменено, главное меню" преимущество чат остаётся чистым
        "✅ Действие отменено.\n\n"

        "Главное меню:",

        reply_markup=main_menu()

    )



    await callback.answer()

