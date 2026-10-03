import logging

from aiogram import Bot
from aiogram.types import Message

logger = logging.getLogger(__name__)

async def delete_message(message: Message) -> None:
    """
    Безопасно удаляет сообщение.
    """
    try:
        await message.delete()
    except Exception:
        logger.warning(
            "не удалось удалить сообщение: chat_id=%s message_id=%s",
            message.chat.id,
            message.message_id,
            exc_info=True
        )

async def delete_audio(
    bot: Bot,
    chat_id: int,
    message_id: int | None,
) -> None:

    if not message_id:
        return
    try:
        await bot.delete_message(
            chat_id=chat_id,
            message_id=message_id,
        )
    except Exception:
        logger.warning(
            "не удалось удалить аудио: chat_id=%s message_id=%s",
            chat_id,
            message_id,
            exc_info=True,
        )

async def cleanup_word_message(message, bot, audio_message_id):
    """
    Удаляет старую карточку слова
    и её озвучку
    """

    await delete_message(message)

    await delete_audio(
        bot=bot,
        chat_id=message.chat.id,
        message_id=audio_message_id,
    )

    
ERROR_MESSAGES = {
    "history_not_found":
        "❌ Перевод не найден.",

     "word_not_found":
        "❌ Слово не найдено в словаре.",    
}


def get_error_message(error: str) -> str:

    return ERROR_MESSAGES.get(error, "❌ Неизвестная ошибка.")    