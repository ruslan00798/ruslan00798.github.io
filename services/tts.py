import asyncio
import logging
import os
import tempfile

import edge_tts


logger = logging.getLogger(__name__)


# ==========================================
# Голоса Edge TTS
# ==========================================

VOICES = {
    "en": "en-US-JennyNeural",
    "de": "de-DE-ConradNeural",
    "ru": "ru-RU-SvetlanaNeural",
    "ar": "ar-SA-HamedNeural",
    "fr": "fr-FR-DeniseNeural",
    "es": "es-ES-ElviraNeural",
    "it": "it-IT-ElsaNeural",
    "tr": "tr-TR-EmelNeural",
    "uk": "uk-UA-PolinaNeural",
}


MAX_TTS_LENGTH = 3000
TTS_TIMEOUT = 30


# ==========================================
# Получить голос по языку
# ==========================================

def get_voice(language: str) -> str | None:

    voice = VOICES.get(language)

    if not voice:

        logger.error(
            "Голос для языка не найден: %s",
            language,
        )

        return None

    return voice


# ==========================================
# Text → Speech
# ==========================================

async def text_to_speech(
    text: str,
    voice: str,
) -> str:

    text = text.strip()

    if not text:
        raise ValueError(
            "Пустой текст для озвучки"
        )

    # Ограничение Edge TTS
    if len(text) > MAX_TTS_LENGTH:

        logger.warning(
            "Текст слишком длинный (%s символов), "
            "обрезаем до %s",
            len(text),
            MAX_TTS_LENGTH,
        )

        text = text[:MAX_TTS_LENGTH]

    # Создаём временный mp3
    file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3",
    )

    file_path = file.name
    file.close()

    try:

        logger.info(
            "TTS: voice=%s text=%s",
            voice,
            text,
        )

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
        )

        await asyncio.wait_for(
            communicate.save(file_path),
            timeout=TTS_TIMEOUT,
        )

        # Проверяем, что файл реально создан
        if not os.path.exists(file_path):

            raise RuntimeError(
                "Edge TTS не создал аудиофайл"
            )

        # Проверяем, что файл не пустой
        if os.path.getsize(file_path) == 0:

            raise RuntimeError(
                "Edge TTS создал пустой аудиофайл"
            )

        logger.info(
            "TTS успешно создан: %s",
            file_path,
        )

        return file_path

    except Exception:

        logger.exception(
            "Ошибка Edge TTS: voice=%s",
            voice,
        )

        if os.path.exists(file_path):
            os.remove(file_path)

        raise


# ==========================================
# Основная функция
# ==========================================

async def generate_audio(
    text: str,
    language: str,
) -> str:

    """
    Создаёт MP3-аудио для текста
    на выбранном языке.
    """

    voice = get_voice(language)

    if not voice:

        raise ValueError(
            f"Неподдерживаемый язык озвучки: {language}"
        )

    return await text_to_speech(
        text=text,
        voice=voice,
    )
