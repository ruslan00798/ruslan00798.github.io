from dataclasses import dataclass
from enum import Enum


class TranslationError(str, Enum):
    EMPTY_TEXT = "empty_text"
    LANGUAGE_NOT_SELECTED = "language_not_selected"
    TRANSLATION_FAILED = "translation_failed"

@dataclass(slots=True)
class TranslationResult:
    translated: str | None = None
    history_id: int | None = None
    error: TranslationError | None = None 

    @property
    def success(self) -> bool:
        return self.error is None

@dataclass(slots=True)
class TranslationHistory:
    id: int
    translated_text: str

@dataclass(slots=True)
class AudioResult:
    file_path: str
    text: str          