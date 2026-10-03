import pytest

from unittest.mock import AsyncMock

from services.learning.constants import MODE_ERRORS, MODE_NEW, MODE_REVIEW
from services.learning_service import LearningService
from utils.xp import calculate_study_xp


async def test_process_answer_correct_answer():
    repository = AsyncMock()

    repository.get_word.return_value = {
    "id": 1,
    "word": "house",
    "translation": "дом",
   }

    service = LearningService(repository)

    result = await service.process_answer(
        user_id=123,
        word_id=1,
        mode="new",
        answer="дом"
    )

    assert result.correct is True

    repository.save_word_answer.assert_awaited_once_with(
        123,
        1,
        True
    )

    repository.add_xp.assert_awaited_once_with(
        123,
        calculate_study_xp(True),
    )

    repository.update_session_result.assert_not_awaited()

async def test_process_answer_updates_session():
    repository = AsyncMock()

    repository.get_word.return_value = {
        "id": 1,
        "word": "house",
        "translation": "дом",
    }

    repository.get_language.return_value = None
  

    service = LearningService(repository)

    result = await service.process_answer(
        user_id=123,
        word_id=1,
        mode="new",
        answer="дом",
        update_session=True,
    )

    assert result.correct is True

    repository.update_session_result.assert_awaited_once_with(
        user_id=123,
        correct=True,
    )

async def test_process_answer_wrong_answer():
    repository = AsyncMock()

    repository.get_word.return_value = {
        "id": 1,
        "word": "house",
        "translation": 'дом',
    }

    service = LearningService(repository)  

    result = await service.process_answer(
        user_id=123,
        word_id=1,
        mode="new",
        answer="машина",
    )

    assert result.correct is False

    repository.save_word_answer.assert_awaited_once_with(
        123,
        1,
        False,
    )

    repository.add_xp.assert_awaited_once_with(
        123,
        calculate_study_xp(False)
    )   

async def test_process_answer_word_not_found():
    repository = AsyncMock()

    repository.get_word.return_value = None

    service = LearningService(repository)

    result = await service.process_answer(
        user_id=123,
        word_id=999,
        mode="new",
        answer="дом",
    )

    assert result.correct is False
    assert result.next_word is None
    assert result.finished is False
    assert result.word is None

    repository.save_word_answer.assert_not_awaited()
    repository.add_xp.assert_not_awaited()

async def test_process_answer_does_not_update_session():
    repository = AsyncMock()

    repository.get_word.return_value = {
        "id": 1,
        "word": "house",
        "translation": "дом",
    }

    repository.get_language.return_value = None

    service = LearningService(repository)

    result = await service.process_answer(
        user_id=123,
        word_id=1,
        mode=MODE_NEW,
        answer="дом",
    )

    assert result.correct is True

    repository.update_session_result.assert_not_awaited()

async def test_process_answer_with_correct_flag():
    repository = AsyncMock()

    repository.get_word.return_value = {
        "id":1,
        "word": "house",
        "translation": "дом",
    }

    repository.get_language.return_value = None

    service = LearningService(repository)

    result = await service.process_answer(
        user_id=123,
        word_id=1,
        mode=MODE_NEW,
        correct=True,
    )

    assert result.correct is True

    repository.save_word_answer.assert_awaited_once_with(
        123,
        1,
        True,
    )

    repository.add_xp.assert_awaited_once_with(
        123,
        calculate_study_xp(True)
    )

async def test_process_answer_raises_without_answer_or_correct():
    repository = AsyncMock()

    repository.get_word.return_value = {
        "id": 1,
        "word": "house",
        "translation": "дом",
    }

    service = LearningService(repository)

    with pytest.raises(
        ValueError,
        match="Не передан answer или correct",
    ):
        await service.process_answer(
            user_id=123,
            word_id=1,
            mode=MODE_NEW,
        )

    repository.save_word_answer.assert_not_awaited()
    repository.add_xp.assert_not_awaited()
    repository.update_session_result.assert_not_awaited()

async def test_process_answer_answer_has_priority_over_correct():
    repository = AsyncMock()

    repository.get_word.return_value = {
        "id": 1,
        "word": "house",
        "translation": "дом",
    }

    repository.get_language.return_value = None

    service = LearningService(repository)

    result = await service.process_answer(
        user_id=123,
        word_id=1,
        mode=MODE_NEW,
        answer="дом",
        correct=False,
    )

    assert result.correct is True

    repository.save_word_answer.assert_awaited_once_with(
        123,
        1,
        True,
    )

        
async def test_process_answer_returns_next_word():
    repository = AsyncMock()

    current_word = {
        "id": 1,
        "word": "house",
        "translation": "дом",
    }

    next_word = {
        "id": 2,
        "word": "car",
        "translation": "машина",
    }

    repository.get_word.return_value = current_word
    repository.get_language.return_value = "en"
    repository.get_learning_session.return_value = {
        "category": "general",
        "level": "A1",
    }

    repository.get_random_word.return_value = next_word

    service = LearningService(repository)

    result = await service.process_answer(
        user_id=123,
        word_id=1,
        mode=MODE_NEW,
        answer="дом",
    )

    assert result.correct is True
    assert result.word == current_word
    assert result.next_word == next_word
    assert result.finished is False

    repository.get_random_word.assert_awaited_once_with(
        123,
        "en",
        "general",
        "A1",
    )

"""
Правильный ответ → True
Неправильный ответ → False
update_session=True → сессия обновляется
update_session=False → сессия не обновляется
Слово не найдено → ничего не сохраняется
Передан correct напрямую
Нет ни answer, ни correct → ValueError
answer имеет приоритет над correct
Есть следующее слово → оно попадает в result.next_word

"""

async def test_start_new_learning_returns_none_when_language_not_found():
    repository = AsyncMock()

    repository.get_language.return_value = None

    service =  LearningService(repository)

    result = await service.start_new_learning(
        user_id=123,
        category="general",
        level="A1",
    )

    assert result is None

    repository.save_learning_session.assert_not_awaited()
    repository.get_random_word.assert_not_awaited()
    repository.add_word_progress.assert_not_awaited()

async def test_start_new_learning_returns_word():
    repository = AsyncMock()

    word = {
        "id": 10,
        "word": "house",
        "translation": "дом"
    }

    repository.get_language.return_value = "en"
    repository.get_random_word.return_value = word

    service = LearningService(repository)

    result = await service.start_new_learning(
        user_id=123,
        category="general",
        level="A1",
    )

    assert result == {
        "word": word,
        "mode": MODE_NEW
    }

    repository.save_learning_session.assert_awaited_once_with(
        123,
        category="general",
        level="A1",
    )

    repository.get_random_word.assert_awaited_once_with(
        user_id=123,
        language="en",
        category="general",
        level="A1",
    )

    repository.add_word_progress.assert_awaited_once_with(
        123,
        10,
    )

async def test_start_new_learning_returns_none_when_word_not_found():
    repository = AsyncMock()

    repository.get_language.return_value = "en"
    repository.get_random_word.return_value = None

    service = LearningService(repository)

    result = await service.start_new_learning(
            user_id=123,
            category="general",
            level="A1",
        )
    
    assert result is None

    repository.save_learning_session.assert_awaited_once_with(
        123,
        category="general",
        level="A1",
    )

    repository.get_random_word.assert_awaited_once_with(
        user_id=123,
        language="en",
        category="general",
        level="A1",
    )

    repository.add_word_progress.assert_not_awaited()
        

async def test_finish_learning_returns_none_when_session_not_found():

    repository = AsyncMock()

    repository.finish_session.return_value = None

    service = LearningService(repository)

    result = await service.finish_learning(user_id=123)

    assert result is None

    repository.finish_session.assert_awaited_once_with(123)

async def test_finish_learning_returns_session():

    repository = AsyncMock()

    session = {
        "category": "general",
        "level": "A1",
    }

    repository.finish_session.return_value = session

    service = LearningService(repository)

    result = await service.finish_learning(user_id=123) 

    assert result == session

    repository.finish_session.assert_awaited_once_with(123)


async def test_get_word_returns_word():
    repository = AsyncMock()

    word = {
        "id": 10,
        "word": "house",
        "translation": "дом",
    }

    repository.get_word.return_value = word

    service = LearningService(repository)

    result = await service.get_word(word_id=10)

    assert result == word

    repository.get_word.assert_awaited_once_with(10)


async def test_get_word_returns_none_when_word_not_found():
    repository = AsyncMock()
   
    repository.get_word.return_value = None

    service = LearningService(repository)

    result = await service.get_word(word_id=10)

    assert result is None

    repository.get_word.assert_awaited_once_with(10)

async def test_process_picture_answer_returns_none_when_word_not_found():
    repository = AsyncMock()

    repository.get_word.return_value = None

    service = LearningService(repository)

    result = await service.process_picture_answer(
        user_id=123,
        word_id=10,
        answer="house",
    )
    

    assert result == (None, None)

    repository.get_word.assert_awaited_once_with(10)
    repository.save_word_answer.assert_not_awaited()
    repository.add_xp.assert_not_awaited()

async def test_process_picture_answer_correct_answer():
    repository = AsyncMock()

    word = {
    "id": 10,
    "word": "house",
    "translation": "дом",
    }

    repository.get_word.return_value = word

    service = LearningService(repository)

    result = await service.process_picture_answer(
        user_id=123,
        word_id=10,
        answer="house",
    )

    assert result == (word, True)

    repository.save_word_answer.assert_awaited_once_with(
        123,
        10,
        True,
    )

    repository.add_xp.assert_awaited_once_with(
    123,
    calculate_study_xp(True),
    )

async def test_process_picture_answer_wrong_answer():
    repository = AsyncMock()
    
    word = {
    "id": 10,
    "word": "house",
    "translation": "дом",
    }

    repository.get_word.return_value = word

    service = LearningService(repository)

    result = await service.process_picture_answer(
        user_id=123,
        word_id=10,
        answer="car",
    )

    assert result == (word, False)

    repository.save_word_answer.assert_awaited_once_with(
        123,
        10,
        False,
    )

    repository.add_xp.assert_awaited_once_with(
    123,
    calculate_study_xp(False),
    )

async def test_process_picture_answer_ignores_case_and_spaces():
    repository = AsyncMock()

    word = {
        "id": 10,
        "word": "house",
        "translation": "дом",
        }

    
    repository.get_word.return_value = word

    service = LearningService(repository)
    
    result = await service.process_picture_answer(
            user_id=123,
            word_id=10,
            answer=" HOUSE ",
        )

    assert result == (word, True)

    repository.save_word_answer.assert_awaited_once_with(
            123,
            10,
            True,
        )
    
    repository.add_xp.assert_awaited_once_with(
        123,
        calculate_study_xp(True),
        )

async def test_process_picture_answer_empty_answer():
    repository = AsyncMock()

    word = {
        "id": 10,
        "word": "house",
        "translation": "дом",
        }

    
    repository.get_word.return_value = word

    service = LearningService(repository)
    
    result = await service.process_picture_answer(
            user_id=123,
            word_id=10,
            answer="  ",
        )

    assert result == (word, False)

    repository.save_word_answer.assert_awaited_once_with(
            123,
            10,
            False,
        )
    
    repository.add_xp.assert_awaited_once_with(
        123,
        calculate_study_xp(False),
        )

async def test_prepare_picture_word_returns_word():
    repository = AsyncMock()

    word = {
        "id": 10,
        "word": "house",
        "translation": "дом",
        "image": "house.jpg",
    }

    repository.get_random_picture_word.return_value = word

    service = LearningService(repository)

    result = await service.prepare_picture_word()

    assert result == word

    repository.get_random_picture_word.assert_awaited_once_with()

async def test_prepare_picture_word_returns_none_when_word_not_found():
    repository = AsyncMock()

    repository.get_random_picture_word.return_value = None

    service = LearningService(repository)

    result = await service.prepare_picture_word()

    assert result is None

    repository.get_random_picture_word.assert_awaited_once_with()

async def test_get_next_word_returns_none_when_language_not_found():
    repository = AsyncMock()

    repository.get_language.return_value = None

    service = LearningService(repository)

    result = await service.get_next_word(
        user_id=123,
        mode= MODE_ERRORS,
    )

    assert result is None

    repository.get_learning_session.assert_not_awaited()

async def test_get_next_word_errors_mode():
    repository = AsyncMock()
    
    repository.get_language.return_value = "en"

    word = {
    "id": 20,
    "word": "car",
    "translation": "машина",
    }

    repository.get_random_wrong_word.return_value = word

    service = LearningService(repository)

    result = await service.get_next_word(
        user_id=123,
        mode=MODE_ERRORS,
    )

    assert result == word

    repository.get_random_wrong_word.assert_awaited_once_with(
    123,
    "en",
   )

async def test_get_next_word_review_mode():
    repository = AsyncMock()
        
    repository.get_language.return_value = "en"

    word = {
    "id": 20,
    "word": "car",
    "translation": "машина",
    }

    repository.get_review_word.return_value = word

    service = LearningService(repository)

    result = await service.get_next_word(
        user_id=123,
        mode=MODE_REVIEW,
    )

    assert result == word

    repository.get_review_word.assert_awaited_once_with(
    123,
    "en",
    )

async def test_get_next_word_returns_none_when_session_not_found():
    repository = AsyncMock()

    repository.get_language.return_value = "en"

    repository.get_learning_session.return_value = None

    service = LearningService(repository)

    result = await service.get_next_word(
        user_id=123,
        mode=MODE_NEW
    )

    assert result is None

    repository.save_word_answer.assert_not_awaited()

async def test_get_next_word_returns_random_word():
    repository = AsyncMock()

    repository.get_language.return_value = "en"

    session = {
        "category": "general",
        "level": "A1",
    }

    repository.get_learning_session.return_value = session

    word = {
        "id": 10,
        "word": "house",
        "translation": "дом",
    }

    repository.get_random_word.return_value = word

    service = LearningService(repository)

    result = await service.get_next_word(
        user_id=123,
        mode=MODE_NEW,
    )

    assert result == word

    repository.get_random_word.assert_awaited_once_with(
        123,
        "en",
        "general",
        "A1"
    )

async def test_save_word_result_correct_answer():
    repository = AsyncMock()

   
    service = LearningService(repository)

    await service.save_word_result(
        user_id=123,
        word_id=10,
        correct=True,
    )

    repository.save_word_answer.assert_awaited_once_with(
        123,
        10,
        True
    )

    repository.add_xp.assert_awaited_once_with(
        123,
        calculate_study_xp(True)
    )

async def test_save_word_result_wrong_answer():
    repository = AsyncMock()

   
    service = LearningService(repository)

    await service.save_word_result(
        user_id=123,
        word_id=10,
        correct=False
    )

    repository.save_word_answer.assert_awaited_once_with(
        123,
        10,
        False
    )

    repository.add_xp.assert_awaited_once_with(
        123,
        calculate_study_xp(False)
    )






    
    


        



    


    




    
    
    



    


        













    






















    










        

    