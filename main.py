import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from config import settings
from database.requests import connect_db, close_db
from database.redis_client import redis

from utils.logger import setup_logger

from handlers.start import start_router
from handlers.menu import menu_router
from handlers.cancel import cancel_router
from handlers.language import language_router
from handlers.settings import settings_router
from handlers.document import document_router
from handlers.history import history_router
from handlers.profile import profile_router

from handlers.learn import learn_router
from handlers.translate import translate_router

from handlers.voice import voice_router
from handlers.pictury import picture_router
from handlers.review import review_router


async def main():

    setup_logger()

    # ======================
    # Подключение к БД
    # ======================

    await connect_db()

    # ======================
    # Подключение Redis
    # ======================

    storage = RedisStorage(redis=redis)

    # ======================
    # Telegram Bot
    # ======================

    bot = Bot(token=settings.bot_token)

    dp = Dispatcher(storage=storage)

    # ======================
    # Регистрация роутеров
    # ======================

    # Основные команды
    dp.include_router(start_router)

    # Настройка пользователя
    dp.include_router(language_router)
    dp.include_router(settings_router)
    dp.include_router(profile_router)

    # Главное меню и общие действия
    dp.include_router(menu_router)
    dp.include_router(cancel_router)

    # Обучение
    dp.include_router(learn_router)
    dp.include_router(review_router)

    # Дополнительные функции обучения
    dp.include_router(picture_router)
    dp.include_router(voice_router)

    # Работа с текстом и документами
    dp.include_router(translate_router)
    dp.include_router(document_router)
    dp.include_router(history_router)

    # ======================
    # Запуск бота
    # ======================

    try:

        await dp.start_polling(bot)

    finally:
        await close_db
        await redis.aclose()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
