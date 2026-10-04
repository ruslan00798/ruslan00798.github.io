import asyncio
import logging
import os
import tempfile

import edge_tts
from edge_tts.exceptions import NoAudioReceived


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


# ==========================================
# Настройки
# ==========================================

MAX_TTS_LENGTH = 3000
TTS_TIMEOUT = 30
TTS_RETRIES = 3
TTS_RETRY_DELAY = 2


# ==========================================
# Получить голос по языку
# ==========================================

def get_voice(language: str) -> str | None:
    """
    Возвращает голос Edge TTS для языка.
    """

    voice = VOICES.get(language)

    if not voice:
        logger.error(
            "Голос для языка не найден: language=%s",
            language,
        )

        return None

    return voice


# ==========================================
# Text -> Speech
# ==========================================

async def text_to_speech(
    text: str,
    voice: str,
) -> str:
    """
    Преобразует текст в MP3.

    Возвращает путь к MP3-файлу.

    Важно:
    после успешного выполнения файл НЕ удаляется.
    Его должен удалить вызывающий код после отправки
    аудио пользователю в Telegram.
    """

    # ------------------------------------------
    # Проверяем текст
    # ------------------------------------------

    text = text.strip()

    if not text:
        raise ValueError(
            "Пустой текст для озвучки"
        )

    # ------------------------------------------
    # Проверяем голос
    # ------------------------------------------

    if not voice:
        raise ValueError(
            "Не указан голос для TTS"
        )

    # ------------------------------------------
    # Ограничение длины
    # ------------------------------------------

    if len(text) > MAX_TTS_LENGTH:
        logger.warning(
            "Текст слишком длинный: %s символов, "
            "обрезаем до %s",
            len(text),
            MAX_TTS_LENGTH,
        )

        text = text[:MAX_TTS_LENGTH].rstrip()

    logger.info(
        "TTS started: voice=%s text_length=%s",
        voice,
        len(text),
    )

    last_error: Exception | None = None

    # ==========================================
    # Повторные попытки
    # ==========================================

    for attempt in range(1, TTS_RETRIES + 1):

        file_path: str | None = None

        try:
            # ----------------------------------
            # Создаём временный MP3
            # ----------------------------------

            file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3",
            )

            file_path = file.name
            file.close()

            logger.info(
                "TTS attempt=%s/%s voice=%s",
                attempt,
                TTS_RETRIES,
                voice,
            )

            # ----------------------------------
            # Создаём Edge TTS
            # ----------------------------------

            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
            )

            # ----------------------------------
            # Генерируем аудио с timeout
            # ----------------------------------

            await asyncio.wait_for(
                communicate.save(file_path),
                timeout=TTS_TIMEOUT,
            )

            # ----------------------------------
            # Проверяем существование файла
            # ----------------------------------

            if not os.path.exists(file_path):
                raise RuntimeError(
                    "Edge TTS не создал аудиофайл"
                )

            # ----------------------------------
            # Проверяем размер файла
            # ----------------------------------

            file_size = os.path.getsize(file_path)

            if file_size == 0:
                raise RuntimeError(
                    "Edge TTS создал пустой аудиофайл"
                )

            logger.info(
                "TTS успешно создан: "
                "voice=%s size=%s bytes",
                voice,
                file_size,
            )

            # ----------------------------------
            # УСПЕХ
            #
            # Файл НЕ удаляем.
            # Его должен удалить код,
            # который отправляет его в Telegram.
            # ----------------------------------

            return file_path

        # ======================================
        # Edge TTS не вернул аудио
        # ======================================

        except NoAudioReceived as error:

            last_error = error

            logger.warning(
                "Edge TTS не вернул аудио: "
                "attempt=%s/%s voice=%s",
                attempt,
                TTS_RETRIES,
                voice,
            )

        # ======================================
        # Timeout
        # ======================================

        except asyncio.TimeoutError as error:

            last_error = error

            logger.warning(
                "Edge TTS timeout: "
                "attempt=%s/%s voice=%s timeout=%s",
                attempt,
                TTS_RETRIES,
                voice,
                TTS_TIMEOUT,
            )

        # ======================================
        # Остальные ошибки
        # ======================================

        except Exception as error:

            last_error = error

            logger.exception(
                "Ошибка Edge TTS: "
                "attempt=%s/%s voice=%s",
                attempt,
                TTS_RETRIES,
                voice,
            )

        # ======================================
        # Удаляем файл неудачной попытки
        # ======================================

        if file_path and os.path.exists(file_path):

            try:
                os.remove(file_path)

                logger.debug(
                    "Удалён временный файл неудачной "
                    "попытки: %s",
                    file_path,
                )

            except OSError:

                logger.warning(
                    "Не удалось удалить временный файл: %s",
                    file_path,
                )

        # ======================================
        # Ждём перед повторной попыткой
        # ======================================

        if attempt < TTS_RETRIES:

            logger.info(
                "Повторная попытка TTS через %s сек.",
                TTS_RETRY_DELAY,
            )

            await asyncio.sleep(
                TTS_RETRY_DELAY
            )

    # ==========================================
    # Все попытки завершились ошибкой
    # ==========================================

    logger.error(
        "Edge TTS окончательно не смог "
        "создать аудио: voice=%s attempts=%s",
        voice,
        TTS_RETRIES,
    )

    if last_error:
        raise last_error

    raise RuntimeError(
        "Edge TTS не смог создать аудио"
    )


# ==========================================
# Основная функция
# ==========================================

async def generate_audio(
    text: str,
    language: str,
) -> str:
    
    # ------------------------------------------
    # Получаем голос
    # ------------------------------------------

    voice = get_voice(language)

    if not voice:
        raise ValueError(
            f"Неподдерживаемый язык озвучки: {language}"
        )

    # ------------------------------------------
    # Генерируем аудио
    # ------------------------------------------

    return await text_to_speech(
        text=text,
        voice=voice,
    )