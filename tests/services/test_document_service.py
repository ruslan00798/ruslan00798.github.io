from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.types import Document

import services.document_service as document_service

from services.document_service import (
    DocumentService,
    MAX_TEXT_LENGTH,
    cleanup_file,
    validate_format,
    UnsupportedFormatError,
    validate_text,
    EmptyDocumentError,
    DocumentTooLargeError,
)


@pytest.mark.parametrize(
    "filename",
    [
        "document.txt",
        "document.docx",
        "document.pdf",
        "document.pptx",
        "document.xlsx",
    ],
)
def test_validate_format_accepts_supported_format(filename):
    validate_format(filename)


def test_validate_format_rejects_exe():
    with pytest.raises(
        UnsupportedFormatError,
        match="Неподдерживаемый формат: \\.exe",
    ):
        validate_format("document.exe")


def test_validate_text_accepts_normal_text():
    validate_text("Это обычный текст документа.")


def test_validate_text_rejects_empty_text():
    with pytest.raises(
        EmptyDocumentError,
        match="Документ пуст.",
    ):
        validate_text("")


def test_validate_text_rejects_whitespace_only_text():
    with pytest.raises(
        EmptyDocumentError,
        match="Документ пуст.",
    ):
        validate_text("  ")


def test_validate_text_rejects_text_over_max_length():
    text = "a" * 20_001

    with pytest.raises(
        DocumentTooLargeError,
        match=f"Документ содержит более {MAX_TEXT_LENGTH} символов.",
    ):
        validate_text(text)


def test_validate_text_max_length():
    text = "a" * 20_000

    validate_text(text)


def test_cleanup_file_removes_existing_file(tmp_path):
    file_path = tmp_path / "test.txt"

    file_path.write_text("test")

    assert file_path.exists()

    cleanup_file(file_path)

    assert not file_path.exists()


def test_cleanup_file_ignores_missing_file(tmp_path):
    file_path = tmp_path / "test.txt"

    assert not file_path.exists()

    cleanup_file(file_path)


async def test_process_document_rejects_document_without_filename():
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(ValueError) as exc_info:
        await service.process_document(
            None,
            document,
            "ru",
        )

    assert str(exc_info.value) == "Документ не содержит имени файла."


async def test_process_document_rejects_unsupported_format():
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.exe",
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(UnsupportedFormatError) as exc_info:
        await service.process_document(
            None,
            document,
            "ru",
        )

    assert str(exc_info.value) == "Неподдерживаемый формат: .exe"


async def test_process_document_success(tmp_path, monkeypatch):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.touch()

    bot.download.side_effect = fake_download

    read_document_mock = Mock(
        return_value="Hello world",
    )

    monkeypatch.setattr(
        document_service,
        "read_document",
        read_document_mock,
    )

    translate_mock = AsyncMock(
        return_value="Привет мир",
    )

    monkeypatch.setattr(
        document_service,
        "translate",
        translate_mock,
    )

    save_document_mock = Mock()

    monkeypatch.setattr(
        document_service,
        "save_document",
        save_document_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    result = await service.process_document(
        bot,
        document,
        "ru",
    )

    bot.download.assert_awaited_once()

    download_args = bot.download.await_args

    assert download_args.args[0] is document
    assert download_args.kwargs["destination"].parent == tmp_path

    input_path = download_args.kwargs["destination"]

    read_document_mock.assert_called_once_with(input_path)

    translate_mock.assert_awaited_once_with(
        "Hello world",
        "ru",
    )

    save_document_mock.assert_called_once()

    save_args = save_document_mock.call_args

    assert save_args.args[0] == "Привет мир"
    assert save_args.args[1] == input_path

    output_path = save_args.args[2]

    assert result == output_path
    assert result.parent == tmp_path
    assert result.name.endswith("_translated.txt")


async def test_process_document_raises_when_file_not_downloaded(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        FileNotFoundError,
        match="Документ не скачан",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    bot.download.assert_awaited_once()


async def test_process_document_raises_when_read_document_fails(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    read_document_mock = Mock(
        side_effect=RuntimeError("Ошибка чтения"),
    )

    monkeypatch.setattr(
        document_service,
        "read_document",
        read_document_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        RuntimeError,
        match="Ошибка чтения",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    read_document_mock.assert_called_once()

    assert list(tmp_path.iterdir()) == []


async def test_process_document_rejects_empty_document(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    read_document_mock = Mock(
        return_value=" ",
    )

    monkeypatch.setattr(
        document_service,
        "read_document",
        read_document_mock,
    )

    translate_mock = AsyncMock()

    monkeypatch.setattr(
        document_service,
        "translate",
        translate_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        EmptyDocumentError,
        match="Документ пуст.",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    read_document_mock.assert_called_once()

    translate_mock.assert_not_awaited()

    assert list(tmp_path.iterdir()) == []


async def test_process_document_rejects_too_large_document(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("text")

    bot.download.side_effect = fake_download

    large_text = "a" * (MAX_TEXT_LENGTH + 1)

    read_document_mock = Mock(
        return_value=large_text,
    )

    monkeypatch.setattr(
        document_service,
        "read_document",
        read_document_mock,
    )

    translate_mock = AsyncMock()

    monkeypatch.setattr(
        document_service,
        "translate",
        translate_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        DocumentTooLargeError,
        match=f"Документ содержит более {MAX_TEXT_LENGTH} символов.",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    translate_mock.assert_not_awaited()

    assert list(tmp_path.iterdir()) == []


async def test_process_document_raises_when_translate_fails(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    read_document_mock = Mock(
        return_value="Hello world",
    )

    monkeypatch.setattr(
        document_service,
        "read_document",
        read_document_mock,
    )

    translate_mock = AsyncMock(
        side_effect=RuntimeError("Ошибка перевода"),
    )

    monkeypatch.setattr(
        document_service,
        "translate",
        translate_mock,
    )

    save_document_mock = Mock()

    monkeypatch.setattr(
        document_service,
        "save_document",
        save_document_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        RuntimeError,
        match="Ошибка перевода",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    translate_mock.assert_awaited_once_with(
        "Hello world",
        "ru",
    )

    save_document_mock.assert_not_called()

    assert list(tmp_path.iterdir()) == []


async def test_process_document_raises_when_translation_is_empty(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("text")

    bot.download.side_effect = fake_download

    monkeypatch.setattr(
        document_service,
        "read_document",
        Mock(return_value="Hello world"),
    )

    translate_mock = AsyncMock(
        return_value="",
    )

    monkeypatch.setattr(
        document_service,
        "translate",
        translate_mock,
    )

    save_document_mock = Mock()

    monkeypatch.setattr(
        document_service,
        "save_document",
        save_document_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        ValueError,
        match="Перевод не найден.",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    translate_mock.assert_awaited_once_with(
        "Hello world",
        "ru",
    )

    save_document_mock.assert_not_called()

    assert list(tmp_path.iterdir()) == []


async def test_process_document_raises_when_save_document_fails(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("text")

    bot.download.side_effect = fake_download

    monkeypatch.setattr(
        document_service,
        "read_document",
        Mock(return_value="Hello world"),
    )

    monkeypatch.setattr(
        document_service,
        "translate",
        AsyncMock(return_value="Привет мир"),
    )

    save_document_mock = Mock(
        side_effect=RuntimeError("Ошибка сохранения"),
    )

    monkeypatch.setattr(
        document_service,
        "save_document",
        save_document_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        RuntimeError,
        match="Ошибка сохранения",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    save_document_mock.assert_called_once()

    assert list(tmp_path.iterdir()) == []


async def test_process_document_removes_output_file_when_save_fails(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    monkeypatch.setattr(
        document_service,
        "read_document",
        Mock(return_value="Hello world"),
    )

    monkeypatch.setattr(
        document_service,
        "translate",
        AsyncMock(return_value="Привет мир"),
    )

    def fake_save_document(
        translated_text,
        input_path,
        output_path,
    ):
        output_path.write_text("translated")
        raise RuntimeError("Ошибка сохранения")

    monkeypatch.setattr(
        document_service,
        "save_document",
        fake_save_document,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        RuntimeError,
        match="Ошибка сохранения",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    assert list(tmp_path.iterdir()) == []


async def test_process_document_cleans_up_files_when_translate_fails(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    monkeypatch.setattr(
        document_service,
        "read_document",
        Mock(return_value="Hello world"),
    )

    monkeypatch.setattr(
        document_service,
        "translate",
        AsyncMock(
            side_effect=RuntimeError("Ошибка перевода"),
        ),
    )

    cleanup_file_mock = Mock()

    monkeypatch.setattr(
        document_service,
        "cleanup_file",
        cleanup_file_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        RuntimeError,
        match="Ошибка перевода",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    input_path = bot.download.await_args.kwargs["destination"]

    assert cleanup_file_mock.call_count == 2

    cleanup_file_mock.assert_any_call(input_path)


async def test_process_document_cleans_up_files_when_save_document_fails(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    monkeypatch.setattr(
        document_service,
        "read_document",
        Mock(return_value="Hello world"),
    )

    monkeypatch.setattr(
        document_service,
        "translate",
        AsyncMock(return_value="Привет мир"),
    )

    monkeypatch.setattr(
        document_service,
        "save_document",
        Mock(
            side_effect=RuntimeError("Ошибка сохранения"),
        ),
    )

    cleanup_file_mock = Mock()

    monkeypatch.setattr(
        document_service,
        "cleanup_file",
        cleanup_file_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        RuntimeError,
        match="Ошибка сохранения",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    input_path = bot.download.await_args.kwargs["destination"]

    assert cleanup_file_mock.call_count == 2

    cleanup_file_mock.assert_any_call(input_path)


async def test_process_document_calls_save_document_with_correct_arguments(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    monkeypatch.setattr(
        document_service,
        "read_document",
        Mock(return_value="Hello world"),
    )

    monkeypatch.setattr(
        document_service,
        "translate",
        AsyncMock(return_value="Привет мир"),
    )

    save_document_mock = Mock()

    monkeypatch.setattr(
        document_service,
        "save_document",
        save_document_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    result = await service.process_document(
        bot,
        document,
        "ru",
    )

    input_path = bot.download.await_args.kwargs["destination"]

    save_document_mock.assert_called_once()

    save_args = save_document_mock.call_args

    assert save_args.args[0] == "Привет мир"
    assert save_args.args[1] == input_path

    output_path = save_args.args[2]

    assert output_path.parent == tmp_path
    assert "_translated" in output_path.name
    assert output_path.suffix == ".txt"

    assert result == output_path


async def test_process_document_preserves_docx_extension(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.docx",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    monkeypatch.setattr(
        document_service,
        "read_document",
        Mock(return_value="Hello"),
    )

    monkeypatch.setattr(
        document_service,
        "translate",
        AsyncMock(return_value="Привет"),
    )

    save_document_mock = Mock()

    monkeypatch.setattr(
        document_service,
        "save_document",
        save_document_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    result = await service.process_document(
        bot,
        document,
        "ru",
    )

    assert result.suffix == ".docx"
    assert result.name.endswith("_translated.docx")


async def test_process_document_passes_correct_language_to_translate(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    monkeypatch.setattr(
        document_service,
        "read_document",
        Mock(return_value="Hello"),
    )

    translate_mock = AsyncMock(
        return_value="Привет",
    )

    monkeypatch.setattr(
        document_service,
        "translate",
        translate_mock,
    )

    monkeypatch.setattr(
        document_service,
        "save_document",
        Mock(),
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    await service.process_document(
        bot,
        document,
        "en",
    )

    translate_mock.assert_awaited_once_with(
        "Hello",
        "en",
    )


async def test_process_document_removes_input_file_after_success(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    monkeypatch.setattr(
        document_service,
        "read_document",
        Mock(return_value="Hello"),
    )

    monkeypatch.setattr(
        document_service,
        "translate",
        AsyncMock(return_value="Привет"),
    )

    monkeypatch.setattr(
        document_service,
        "save_document",
        Mock(),
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    result = await service.process_document(
        bot,
        document,
        "ru",
    )

    input_path = bot.download.await_args.kwargs["destination"]

    assert not input_path.exists()
    assert result.parent == tmp_path


async def test_process_document_does_not_call_translate_when_read_fails(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    monkeypatch.setattr(
        document_service,
        "read_document",
        Mock(
            side_effect=RuntimeError("Ошибка чтения"),
        ),
    )

    translate_mock = AsyncMock()

    monkeypatch.setattr(
        document_service,
        "translate",
        translate_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        RuntimeError,
        match="Ошибка чтения",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    translate_mock.assert_not_awaited()


async def test_process_document_does_not_call_save_when_translation_is_empty(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    monkeypatch.setattr(
        document_service,
        "read_document",
        Mock(return_value="Hello"),
    )

    translate_mock = AsyncMock(
        return_value=None,
    )

    monkeypatch.setattr(
        document_service,
        "translate",
        translate_mock,
    )

    save_document_mock = Mock()

    monkeypatch.setattr(
        document_service,
        "save_document",
        save_document_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        ValueError,
        match="Перевод не найден.",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    translate_mock.assert_awaited_once_with(
        "Hello",
        "ru",
    )

    save_document_mock.assert_not_called()


async def test_process_document_does_not_call_save_when_read_fails(
    tmp_path,
    monkeypatch,
):
    document = Document(
        file_id="123",
        file_unique_id="unique",
        file_size=100,
        file_name="document.txt",
    )

    monkeypatch.setattr(
        document_service,
        "TEMP_DIR",
        tmp_path,
    )

    bot = Mock()
    bot.download = AsyncMock()

    async def fake_download(document, destination):
        destination.write_text("test")

    bot.download.side_effect = fake_download

    monkeypatch.setattr(
        document_service,
        "read_document",
        Mock(
            side_effect=RuntimeError("Ошибка чтения"),
        ),
    )

    save_document_mock = Mock()

    monkeypatch.setattr(
        document_service,
        "save_document",
        save_document_mock,
    )

    repository = AsyncMock()
    service = DocumentService(repository)

    with pytest.raises(
        RuntimeError,
        match="Ошибка чтения",
    ):
        await service.process_document(
            bot,
            document,
            "ru",
        )

    save_document_mock.assert_not_called()
