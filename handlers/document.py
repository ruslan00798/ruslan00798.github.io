from pathlib import Path # удобная работа с путями к файлам

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

# Получение выбранного пользователем языка из базы данных
from database.requests import get_language

# Клавиатура с кнопкой "Назад"
from keyboards.back_menu_kbd import back_menu_keyboard

# Сервис обработки документа
from services.document_service import(
    process_document,         #Полностью обрабатывает документ
    UnsupportedFormatError,   #Ошибка: неподдерживаемый формат
    EmptyDocumentError,       #Ошибка: документ пуст
    DocumentTooLargeError,    #Ошибка: слишком большой документ
    cleanup_file,             # Удаление временного файла
)

# Состояние FSM
from states.translate_state import TranslateState

document_router = Router()

# Этот обработчик сработает только тогда,
# когда пользователь находится в состоянии waiting_document
# и отправляет документ.
@document_router.message(TranslateState.waiting_document, F.document)
async def translate_document(message: Message, state: FSMContext):

    # Получаем язык перевода пользователя из базы данных
    language = await get_language(message.from_user.id)

    #Если язык не выбран - прекращаем работу
    if not language:
        await message.answer("❗ Сначала выберите язык перевода.")

        return
    
    # Сообщаем пользователю,
    # что документ получен и началась обработка
    await message.answer( "📄 Документ получен.\n" "⏳ Начинаю перевод...")

    # Здесь позже будет храниться путь
    # к готовому переведенному документу.
    translated_path = None

    try:

        #Передаем документ в сервис.
        #Там произойдёт:
        #
        #1. проверка формата;
        #2. создание temp;
        #3. скачивание;
        #4. чтение;
        #5. проверка текста;
        #6. перевод;
        # # 7. сохранение нового файла.
        translated_path = await process_document(
            bot=message.bot,
            document=message.document,
            language=language,
        )

        #Отправляем пользователю готовый документ
        await message.answer_document(
            document=FSInputFile(translated_path),
            caption= "✅ Перевод готов",
            reply_markup=back_menu_keyboard
        )

        #Очищаем состояние FSM.
        #Пользователь завершил перевод.
        await state.clear()
    
    #Пользователь загрузил неподдерживаемый формат
    except UnsupportedFormatError:

        await message.answer( "❌ Неподдерживаемый формат файла.")
    
    #Документ не содержит текста
    except EmptyDocumentError:

        await message.answer("❌ Документ пуст.")

    #Документ превышает допустимый размер
    except DocumentTooLargeError:

        await message.answer(
            "⚠️ Документ слишком большой.\n"
            "Максимум 20 000 символов."
        )

    #Любая другая ошибка
    except Exception:

        await message.answer("❌ Ошибка обработки документа.")  

    # Этот блок выполняется всегда,
    # независимо от того,
    # была ошибка или нет.
    finally:

        #Если переведенный файл существует
        #удаляем его из временной папки.
        if translated_path:

            cleanup_file(Path(translated_path))        
       
         


