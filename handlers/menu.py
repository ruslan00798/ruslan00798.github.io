#menu.py
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states.translate_state import TranslateState
from keyboards.cancel_kbd import cancel_keyboard
from keyboards.menu_kbd import main_menu

menu_router = Router()

logger = logging.getLogger(__name__)


@menu_router.callback_query(F.data == "translate_text")
async def translate_text_mode(
    callback: CallbackQuery,
    state: FSMContext
):
    user_id = callback.from_user.id

    logger.info(
        "tranalate_text_mode_started user_id=%s",
        user_id
    )

    await state.set_state(TranslateState.waiting_text)

    logger.info(
        "translate_text_state_set user_id=%s state=%s",
        user_id,
        TranslateState.waiting_text.state,
    )

    await callback.message.answer(
        "🔤 Режим перевода текста включён.\n\n"
        "Отправьте слово, предложение или текст.",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()

@menu_router.callback_query(F.data == "translate_document")
async def translate_document_mode(
    callback: CallbackQuery,
    state: FSMContext
):
    user_id = callback.from_user.id

    logger.info(
        "translate_document_mode_started user_id=%s",
        user_id
    )
    await state.set_state(TranslateState.waiting_document)

    logger.info(
        "translate_document_state_set user_id=%s state=%s",
        user_id,
        TranslateState.waiting_document.state,
    )
    await callback.message.answer(

        "📄 Режим перевода документов включён.\n\n"

        "Отправьте файл.",

        reply_markup=cancel_keyboard()
    )
    await callback.answer()

@menu_router.callback_query(F.data == "back_menu")
async def back_menu(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.answer(
        "🏠 Главное меню:",
        reply_markup=main_menu()
    )

    await callback.answer()   