from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from services.learning_flow import  send_next_word

from services.learning_flow import start_review_mode





review_router = Router()


@review_router.callback_query(F.data == "repeat_errors")
async def repeat_errors(callback: CallbackQuery, state: FSMContext):
   
   await start_review_mode(
      callback=callback,
      state=state,
      mode="errors"
   )

   await callback.answer()


@review_router.callback_query(F.data == "study_words")
async def study_words(callback: CallbackQuery, state: FSMContext):

    await start_review_mode(
        callback=callback,
        state=state,
        mode="review"
    )

    await callback.answer()

@review_router.callback_query(F.data == "next_review_word")
async def next_review_word(callback: CallbackQuery, state:FSMContext):
    
    await send_next_word(callback, state)

    await callback.answer()