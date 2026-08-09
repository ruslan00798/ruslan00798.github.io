import asyncio
import logging


from aiogram import Bot, Dispatcher


from database.requests import connect_db


from config import BOT_TOKEN



from handlers.start import start_router
from handlers.menu import menu_router
from handlers.cancel import cancel_router
from handlers.language import language_router
from handlers.settings import settings_router
from handlers.document import document_router
from handlers.history import history_router
from handlers.profile import profile_router
from handlers.study import study_router
from handlers.learn import learn_router
from handlers.translate import translate_router
from handlers.callback import callbacks_router
from handlers.voice import voice_router
from handlers.pictury import picture_router
from handlers.review import review_router


logging.basicConfig(
    level=logging.INFO
)

async def main():
    # Подключаем БД

    await connect_db()

    bot = Bot(
        token=BOT_TOKEN
    )

    dp = Dispatcher()

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
    dp.include_router(callbacks_router)
    dp.include_router(cancel_router)

    # Обучение
    dp.include_router(learn_router)
    dp.include_router(review_router)
    dp.include_router(study_router)

    # Дополнительные функции обучения
    dp.include_router(picture_router)
    dp.include_router(voice_router)

    # Работа с текстом и документами
    dp.include_router(translate_router)
    dp.include_router(document_router)
    dp.include_router(history_router)

    await dp.start_polling(bot)
   


if __name__ == "__main__":


    asyncio.run(main())
