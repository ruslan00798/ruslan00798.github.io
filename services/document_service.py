import logging
import uuid
from pathlib import Path

from aiogram import Bot
from aiogram.types import Document

from services.document_parser import read_document, SUPPORTED_FORMATS
from services.document_writer import save_document
from services.translator import translate
from services.learning.language_repository import LanguageRepository


logger = logging.getLogger(__name__)


# Константы
TEMP_DIR = Path("temp")
MAX_TEXT_LENGTH = 20_000


class UnsupportedFormatError(Exception):
    """Документ имеет неподдерживаемое расширение."""
    pass


class EmptyDocumentError(Exception):
    """В документе нет текста."""
    pass


class DocumentTooLargeError(Exception):
    """Документ превышает лимит."""
    pass


class DocumentService:
    def __init__(self, repository):
        self.repository = repository
        self.language_repository = LanguageRepository()

    async def get_user_language(self, user_id: int):
        return await self.language_repository.get_language(user_id)
    
    async def process_document(
        self,
        bot: Bot,
        document: Document,
        language: str,
    ) -> Path:
        """
        Полный цикл обработки документа.

        1. Проверяет имя и формат файла.
        2. Создаёт временную папку.
        3. Скачивает документ.
        4. Извлекает текст.
        5. Проверяет текст.
        6. Переводит текст.
        7. Сохраняет новый документ.
        8. Возвращает путь к переведённому файлу.
        """

        if not document.file_name:
            raise ValueError(
                "Документ не содержит имени файла."
            )

        # Проверяем формат
        validate_format(document.file_name)

        # Создаём временную папку
        TEMP_DIR.mkdir(exist_ok=True)

        # Создаём уникальное имя
        unique_id = uuid.uuid4().hex

        input_path = (
            TEMP_DIR /
            f"{unique_id}_{document.file_name}"
        )

        extension = Path(document.file_name).suffix

        output_path = (
            TEMP_DIR /
            f"{unique_id}_translated{extension}"
        )

        try:
            # Скачивание документа
            await bot.download(
                document,
                destination=input_path,
            )

            if not input_path.exists():
                raise FileNotFoundError(
                    "Документ не скачан."
                )

            # Чтение документа
            text = read_document(input_path)

            # Проверка текста
            validate_text(text)

            # Перевод
            translated_text = await translate(
                text,
                language,
            )

            if not translated_text:
                raise ValueError(
                    "Перевод не найден."
                )

            # Создание нового документа
            save_document(
                translated_text,
                input_path,
                output_path,
            )

            return output_path

        except Exception:
            # Если произошла ошибка,
            # удаляем созданный выходной файл.
            cleanup_file(output_path)

            raise

        finally:
            # Входной временный файл
            # удаляется всегда.
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
        raise EmptyDocumentError(
            "Документ пуст."
        )

    if len(text) > MAX_TEXT_LENGTH:
        raise DocumentTooLargeError(
            f"Документ содержит более "
            f"{MAX_TEXT_LENGTH} символов."
        )


def cleanup_file(path: Path) -> None:
    """Удаляет временный файл."""

    try:
        if path.exists():
            path.unlink()

    except Exception:
        logger.exception(
            "Ошибка удаления файла %s",
            path,
        )
