#document.py
import logging
from pathlib import Path # удобная работа с путями к файлам

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message




from keyboards.back_menu_kbd import back_menu_keyboard

# Сервис обработки документа
from services.document_service import(
    DocumentService,
    UnsupportedFormatError,   
    EmptyDocumentError,
    DocumentTooLargeError,   
    cleanup_file,           
)

from services.learning.document_repository import DocumentRepository
from states.translate_state import TranslateState

document_repository = DocumentRepository()
document_service = DocumentService(document_repository)

document_router = Router()

logger = logging.getLogger(__name__)


@document_router.message(TranslateState.waiting_document, F.document)
async def translate_document(message: Message, state: FSMContext):

    user_id = message.from_user.id
    document = message.document

    logger.info(
        "document_translation_started user_id=%s file_name=%s file_size=%s",
        user_id,
        document.file_name,
        document.file_size,
    )

    # Получаем язык перевода пользователя из базы данных
    language = await document_service.get_user_language(message.from_user.id)

    #Если язык не выбран - прекращаем работу
    if not language:
        logger.warning(
            "document_translation_no_language user_id=%s",
            user_id
        )

        await message.answer("❗ Сначала выберите язык перевода.")

        return
    
    await message.answer( "📄 Документ получен.\n" "⏳ Начинаю перевод...")

    translated_path = None

    try:
        translated_path = await document_service.process_document(
            bot=message.bot,
            document=message.document,
            language=language,
        )

        logger.info(
            "document_translation_completed user_id=%s file_name=%s",
            user_id,
            document.file_name,
        )

        await message.answer_document(
            document=FSInputFile(translated_path),
            caption= "✅ Перевод готов",
            reply_markup=back_menu_keyboard(),
        )

        #Очищаем состояние FSM.
        #Пользователь завершил перевод.
        await state.clear()
    
    #Пользователь загрузил неподдерживаемый формат
    except UnsupportedFormatError:

        logger.warning(
            "document_unsupported_format user_id=%s file_name=%s",
            user_id,
            document.file_name,
        )

        await message.answer( "❌ Неподдерживаемый формат файла.")
    
    #Документ не содержит текста
    except EmptyDocumentError:
        logger.warning(
            "document_empty user_id=%s file_name=%s",
            user_id,
            document.file_name
        )

        await message.answer("❌ Документ пуст.")

    #Документ превышает допустимый размер
    except DocumentTooLargeError:
        logger.warning(
            "document_too_large user_id=%s file_name=%s file_size=%s",
            user_id,
            document.file_name,
            document.file_size,
        )

        await message.answer(
            "⚠️ Документ слишком большой.\n"
            "Максимум 20 000 символов."
        )

    #Любая другая ошибка
    except Exception:
        logger.exception(
            "document_translation_failed user_id=%s file_name=%s",
            user_id,
            document.file_name,
        )

        await message.answer("❌ Ошибка обработки документа.")  
   
    finally:

        if translated_path:
            cleanup_file(Path(translated_path))

            logger.info(
                "document_temp_file_cleaned user_id=%s",
                user_id,
            )        
       
         


