import asyncio
import logging

from deep_translator import MyMemoryTranslator
from deep_translator.exceptions import LanguageNotSupportedException
from langdetect import LangDetectException, detect


logger = logging.getLogger(__name__)


LANGUAGE_MAP = {
    "en": "english",
    "de": "german",
    "ru": "russian",
    "fr": "french",
    "es": "spanish",
    "it": "italian",
    "ar": "arabic",
    "tr": "turkish",
    "uk": "ukrainian",
}


SOURCE_LANGUAGE_MAP = {
    "en": "english",
    "de": "german",
    "ru": "russian",
    "fr": "french",
    "es": "spanish",
    "it": "italian",
    "ar": "arabic",
    "tr": "turkish",
    "uk": "ukrainian",
    "mk": "macedonian",
    "bg": "bulgarian",
    "pl": "polish",
    "cs": "czech",
    "sk": "slovak",
    "sl": "slovenian",
    "hr": "croatian",
    "sr": "serbian latin",
    "nl": "dutch",
    "pt": "portuguese",
    "fi": "finnish",
    "sv": "swedish",
    "da": "danish",
    "no": "norwegian bokmål",
    "el": "greek",
    "he": "hebrew",
    "hi": "hindi",
    "id": "indonesian",
    "ja": "japanese",
    "ko": "korean",
    "vi": "vietnamese",
    "th": "thai",
    "ro": "romanian",
    "hu": "hungarian",
    "ca": "catalan",
}


MAX_LENGTH = 4500
REQUEST_DELAY = 0.3


def split_text(
    text: str,
    size: int = MAX_LENGTH,
) -> list[str]:

    text = text.strip()

    if not text:
        return []

    parts = []

    while len(text) > size:

        split_index = text.rfind(" ", 0, size)

        if split_index <= 0:
            split_index = size

        parts.append(
            text[:split_index].strip()
        )

        text = text[split_index:].strip()

    if text:
        parts.append(text)

    return parts


def detect_source_language(
    text: str,
) -> str | None:

    try:

        detected_language = detect(text)

        logger.info(
            "Detected source language: %s",
            detected_language,
        )

        return detected_language

    except LangDetectException:

        logger.exception(
            "Failed to detect source language"
        )

        return None


def get_source_language_name(
    language_code: str,
) -> str | None:

    language = SOURCE_LANGUAGE_MAP.get(
        language_code
    )

    if not language:

        logger.error(
            "Unsupported source language: %s",
            language_code,
        )

        return None

    return language


def translate_part(
    text: str,
    source: str,
    target: str,
) -> str | None:

    try:

        logger.info(
            "MyMemory translation: source=%s target=%s",
            source,
            target,
        )

        translator = MyMemoryTranslator(
            source=source,
            target=target,
        )

        result = translator.translate(text)

        if not result:

            logger.error(
                "MyMemory returned empty result"
            )

            return None

        return result

    except LanguageNotSupportedException:

        logger.exception(
            "MyMemory does not support language: %s",
            source,
        )

        return None

    except Exception:

        logger.exception(
            "MyMemory translation error"
        )

        return None


async def translate(
    text: str,
    language: str,
) -> str | None:

    text = text.strip()

    if not text:
        return ""

    target_language = LANGUAGE_MAP.get(
        language
    )

    if not target_language:

        logger.error(
            "Unsupported target language: %s",
            language,
        )

        return None

    detected_code = detect_source_language(
        text
    )

    if not detected_code:
        return None

    if detected_code == language:

        logger.info(
            "Source and target languages are the same: %s",
            language,
        )

        return text

    source_language = get_source_language_name(
        detected_code
    )

    if not source_language:
        return None

    parts = split_text(text)

    translated_parts = []

    for part in parts:

        translated = await asyncio.to_thread(
            translate_part,
            part,
            source_language,
            target_language,
        )

        if not translated:
            return None

        translated_parts.append(
            translated
        )

        await asyncio.sleep(
            REQUEST_DELAY
        )

    return "\n".join(
        translated_parts
    )


def add_harakat_simple(
    text: str,
) -> str:

    return text
