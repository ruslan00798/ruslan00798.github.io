import logging #используется для записи ошибок
import uuid
from pathlib import Path

from aiogram import Bot
from aiogram.types import Document

from services.document_parser import read_document, SUPPORTED_FORMATS
from services.document_writer import save_document
from services.translator import translate

logger = logging.getLogger(__name__)

#константы
TEMP_DIR = Path("temp") #Информация о временной папке
MAX_TEXT_LENGTH = 20_000 #Информация о временной папке


class UnsupportedFormatError(Exception):
    """
    Документ имеет неподдерживаемое расширение.
    """
    pass

class EmptyDocumentError(Exception): 
    """
    В документе нет текста.
    """
    pass

class DocumentTooLargeError(Exception):
    """
    Документ превышает лимит.
    """  
    pass




#Главная функция

async def process_document(
    bot: Bot,
    document: Document,
    language: str
) -> Path:
 """
    Полный цикл обработки документа.

    1. Проверяет имя и формат файла.
    2. Создает временную папку.
    3. Скачивает документ.
    4. Извлекает текст.
    5. Проверяет текст.
    6. Переводит текст.
    7. Сохраняет новый документ.
    8. Возвращает путь к переведенному файлу.
    """
 
 if not document.file_name:
     raise ValueError("Документ не содержит имени файла.")
 
 
     

 validate_format(document.file_name)


#создаем временную папку
 TEMP_DIR.mkdir(exist_ok=True)

#создание уникального имени    
 unique_id = uuid.uuid4().hex

 input_path = (TEMP_DIR / f"{unique_id}_{document.file_name}")

 extension = (Path(document.file_name).suffix)

 output_path = (TEMP_DIR / f"{unique_id}_translated{extension}")

 try:
      #Скачивание
        await bot.download(document, destination=input_path)

        if not input_path.exists():
            raise FileNotFoundError("документ не скачен")

      #Чтение 
        text = read_document(input_path)

      #Проверка текста
        validate_text(text)

       #перевод 
        translated_text = await translate(text, language)

        if not translated_text:
            raise ValueError("перевод не найден")

       #Создание файла
        save_document(
            translated_text,
            input_path,
            output_path
        )

        return output_path
    

 except Exception:
        #очистка
        cleanup_file(input_path)

        cleanup_file(output_path)

        raise
 
 finally:
     cleanup_file(input_path)


def validate_format(filename: str) -> None:
    """Проверяет расширение файла."""

    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_FORMATS:
        raise UnsupportedFormatError(
            f"Неподдерживаемый формат: {extension}"
        )


def validate_text(text: str) -> None:
    """Проверяет содержимое документа."""
    

    if not text.strip():

        raise EmptyDocumentError("Документ пуст.")
    
    #поверка размера файла
    if len(text) > MAX_TEXT_LENGTH:

        raise DocumentTooLargeError(
            f"Документ содержит более {MAX_TEXT_LENGTH} символов"
        )
    

def cleanup_file(path: Path) -> None:
    """Удаляет временный файл."""

    try:
  
        if path.exists():

            path.unlink()    

    except Exception as error:
        logger.exception("Ошибка удаления файла %s", path)
          
