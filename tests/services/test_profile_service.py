from unittest.mock import AsyncMock, patch
from services.profile_service import ProfileService, ProfileData


@patch("services.profile_service.calculate_level")
@patch("services.profile_service.get_achievements")
async def test_get_profile_data(
    mock_get_achievements,
    mock_calculate_level,
):
    repository = AsyncMock()

    repository.get_statistics.return_value = {
        "translations": 10,
        "favorites": 3,
    }

    repository.get_xp.return_value = 100
    repository.get_learned_words.return_value = 20
    repository.get_language.return_value = "en"

    repository.get_daily_goal.return_value = {
        "completed": 5,
        "target": 10,
    }

    mock_calculate_level.return_value = {
        "level": 2,
        "current_xp": 100,
        "need_xp": 200,
    }

    mock_get_achievements.return_value = [
        "Achievement 1",
        "Achievement 2",
    ]

    service = ProfileService(repository)

    result = await service.get_profile_data(user_id=123)

    assert result.language == "en"
    assert result.xp == 100
    assert result.level == {
        "level": 2,
        "current_xp": 100,
        "need_xp": 200,
    }
    assert result.translations == 10
    assert result.favorites == 3
    assert result.learned_words == 20
    assert result.goal_progress == 5
    assert result.goal_target == 10
    assert result.achievements == [
        "Achievement 1",
        "Achievement 2",
    ]

    repository.get_statistics.assert_awaited_once_with(123)
    repository.get_xp.assert_awaited_once_with(123)
    repository.get_learned_words.assert_awaited_once_with(123)
    repository.get_language.assert_awaited_once_with(123)
    repository.get_daily_goal.assert_awaited_once_with(123)

    mock_calculate_level.assert_called_once_with(100)

    mock_get_achievements.assert_called_once_with(
        10,
        100,
        20,
    )

async def test_get_profile_data_xp_is_none():
    repository = AsyncMock()

    stats = {
        "translations": 10,
        "favorites": 3,
    }

    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = None
    repository.get_learned_words.return_value = 20
    repository.get_language.return_value = "en"

    goal = {
        "completed": 5,
        "target":10,
    }

    repository.get_daily_goal.return_value = goal

    with patch(
        "services.profile_service.calculate_level"
    ) as mock_calculate_level:

        mock_calculate_level.return_value = {
            "level": 1,
            "current_xp": 0,
            "need_xp": 100,
        }

        service = ProfileService(repository)

        result = await service.get_profile_data(user_id=123)

    assert result.xp == 0    



async def test_get_profile_data_xp_is_invalid_string():
    repository = AsyncMock()

    stats = {
        "translations": 10,
        "favorites": 3,
    }

    repository.get_statistics.return_value = stats 
    repository.get_xp.return_value =  "invalid"
    repository.get_learned_words.return_value = 20
    repository.get_language.return_value = "en"

    goal = {
        "completed": 5,
        "target": 10,
    }
    repository.get_daily_goal.return_value = goal

    with patch(
        "services.profile_service.calculate_level"
    ) as mock_calculate_level:

        mock_calculate_level.return_value = {
            "level": 1,
            "current_xp": 0,
            "need_xp": 100,
        }

        service = ProfileService(repository)

        result = await service.get_profile_data(user_id=123)

    assert result.xp == 0

    mock_calculate_level.assert_called_once_with(0)    

async def test_get_profile_data_learned_words_is_none():
    repository = AsyncMock()

    stats = {
            "translations": 10,
            "favorites": 3,
        }
    
    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = 100
    repository.get_learned_words.return_value = None
    repository.get_language.return_value = "en"

    goal = {
            "completed": 5,
            "target": 10,
        }
    
    repository.get_daily_goal.return_value = goal

    with patch(
    "services.profile_service.get_achievements"
    ) as mock_get_achievements:

        mock_get_achievements.return_value = [
            "Achievement 1",
            "Achievement 2",
        ]
            
        

        service = ProfileService(repository)

        result = await service.get_profile_data(user_id=123)

    assert result.learned_words == 0

    mock_get_achievements.assert_called_once_with(
    10,
    100,
    0,
    )

async def test_get_profile_data_learned_words_invalid_string():
    repository = AsyncMock()

    stats = {
            "translations": 10,
            "favorites": 3,
        }
    
    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = 100
    repository.get_learned_words.return_value = "invalid"
    repository.get_language.return_value = "en"

    goal = {
            "completed": 5,
            "target": 10,
        }
    
    repository.get_daily_goal.return_value = goal

    with patch(
    "services.profile_service.get_achievements"
    ) as mock_get_achievements:

        mock_get_achievements.return_value = [
            "Achievement 1",
            "Achievement 2",
        ]

        service = ProfileService(repository)

        result = await service.get_profile_data(user_id=123)

    assert result.learned_words == 0

    mock_get_achievements.assert_called_once_with(
    10,
    100,
    0,
    )

async def test_get_profile_data_goal_is_none():
    repository = AsyncMock()

    stats = {
                "translations": 10,
                "favorites": 3,
            }
        
    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = 100
    repository.get_learned_words.return_value = 20
    repository.get_language.return_value = "en"
    repository.get_daily_goal.return_value = None

    with patch(
        "services.profile_service.calculate_level"
    ) as mock_calculate_level:

        mock_calculate_level.return_value = {
            "level": 2, 
            "current_xp": 100, 
            "need_xp": 200,
        }

        service = ProfileService(repository)

        result = await service.get_profile_data(user_id=123)

    assert result.goal_progress == 0
    assert result.goal_target == 10    

async def test_get_profile_data_goal_is_empty_dict():
    repository = AsyncMock()

    stats = {
        "translations": 10,
        "favorites": 3,
    }
            
    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = 100
    repository.get_learned_words.return_value = 20
    repository.get_language.return_value = "en"
    repository.get_daily_goal.return_value = {}

    with patch(
        "services.profile_service.calculate_level"
    ) as mock_calculate_level:

        mock_calculate_level.return_value = {
            "level": 2, 
            "current_xp": 100, 
            "need_xp": 200,
        }

        service = ProfileService(repository)

        result = await service.get_profile_data(user_id=123)

    assert result.goal_progress == 0
    assert result.goal_target == 10    


async def test_get_profile_data_goal_without_completed():
    repository = AsyncMock()

    stats = {
        "translations": 10,
        "favorites": 3,
    }

    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = 100
    repository.get_learned_words.return_value = 20
    repository.get_language.return_value = "en"

    goal = {
        "target": 20
    }
    repository.get_daily_goal.return_value = goal

    with patch(
        "services.profile_service.calculate_level"
    ) as mock_calculate_level:

        mock_calculate_level.return_value = {
            "level": 2,
            "current_xp": 100,
            "need_xp": 200,
        }

        service = ProfileService(repository)

        result = await service.get_profile_data(user_id=123)

    assert result.goal_progress == 0
    assert result.goal_target == 20 

async def test_get_profile_data_goal_values_are_strings():
    repository = AsyncMock()

    
    stats = {
        "translations": 10,
        "favorites": 3,
    }

    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = 100
    repository.get_learned_words.return_value = 20
    repository.get_language.return_value = "en"

    goal = {
        "completed": "5",
        "target": "20",
    }

    repository.get_daily_goal.return_value = goal

    with patch(
        "services.profile_service.calculate_level"
    ) as mock_calculate_level:

        mock_calculate_level.return_value = {
            "level": 2,
            "current_xp": 100,
            "need_xp": 200,
        }

        service = ProfileService(repository)

        result = await service.get_profile_data(user_id=123)

    assert result.goal_progress == 5
    assert result.goal_target == 20 


def test_build_progress_bar_empty():
    result = ProfileService.build_progress_bar(0, 10)  

    assert result == "░░░░░░░░░░"

def test_build_progress_bar_half(): 
    result = ProfileService.build_progress_bar(5, 10)

    assert result == "█████░░░░░"  

def test_build_progress_bar_full():
    result = ProfileService.build_progress_bar(10, 10)
    
    assert result == "██████████"
    
def test_build_progress_bar_progress_greater_than_targetl():
    result = ProfileService.build_progress_bar(15, 10)
    
    assert result == "██████████"
    
def test_build_progress_bar_target_zero():
    result = ProfileService.build_progress_bar(5, 0)  
    assert result ==  "█████░░░░░"

def test_build_progress_bar_negative_target():
    result = ProfileService.build_progress_bar(5, -5)  
    assert result == "█████░░░░░"  

def test_build_profile_text():
    profile = ProfileData(
        language="en",
        xp=100,
        level={
            "level": 2,
            "current_xp": 100,
            "need_xp": 200,
        },
        translations=10,
        favorites=3,
        learned_words=20,
        goal_progress=5,
        goal_target=10,
        achievements=[
            "Achievement 1",
            "Achievement 2",
        ],
    )
    result = ProfileService.build_profile_text(profile)
    assert "👤 Профиль" in result
    assert "🌐 Язык: en" in result
    assert "🏆 Уровень: 2" in result
    assert "⭐ XP: 100" in result
    assert "📈 До следующего уровня: 100 XP" in result
    assert "📚 Переводов: 10" in result
    assert "⭐ Избранных: 3" in result
    assert "🧠 Изучено слов: 20" in result
    assert "🎯 Цель дня:\n" in result
    assert "█████░░░░░ 5/10" in result
    assert  "🏅 Достижения:\n" in result
    assert "Achievement 1" in result
    assert "Achievement 2" in result

async def test_get_study_progress_text():
    #ARRANGE — подготовили данные
    repository = AsyncMock()

    progress = {
        "total_words": 100,
        "learned_words": 70,
        "difficult_words": 10,
    }

    repository.get_study_progress.return_value = progress

    service = ProfileService(repository)
    #ACT — вызвали функцию
    result = await service.get_study_progress_text(user_id=123)
    #ASSERT — проверили результат
    assert  "📊 Прогресс обучения" in result   
    assert "📝 Всего слов: 100" in result
    assert "✅ Выучено: 70"  in result
    assert "❌ Сложные слова: 10" in result

    repository.get_study_progress.assert_awaited_once_with(123)

async def test_get_study_progress_text_without_total_words():
    repository = AsyncMock()

    progress = {
        "learned_words": 70,
        "difficult_words": 10,
    }

    repository.get_study_progress.return_value = progress

    service = ProfileService(repository)

    
    result = await service.get_study_progress_text(123)

    assert "📝 Всего слов: 0" in result

    repository.get_study_progress.assert_awaited_once_with(123)   

async def test_get_study_progress_text_without_learned_words():
    repository = AsyncMock()

    progress = {
        "total_words": 100,
        "difficult_words": 10,
    }
    repository.get_study_progress.return_value = progress

    service = ProfileService(repository)

    result = await service.get_study_progress_text(user_id=123)

    assert "✅ Выучено: 0" in result

    repository.get_study_progress.assert_awaited_once_with(123)

async def test_get_study_progress_text_without_difficult_words():
    repository = AsyncMock()
    
    progress = {
        "total_words": 100,
        "learned_words": 70,
    }

    repository.get_study_progress.return_value = progress

    service = ProfileService(repository)

    result = await service.get_study_progress_text(user_id=123)

    assert "❌ Сложные слова: 0" in result

    repository.get_study_progress.assert_awaited_once_with(123)

@patch("services.profile_service.get_achievements")  
async def test_get_achievements_text(mock_get_achievements):
    repository = AsyncMock()

    stats = {
        "translations": 10,
    }

    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = 100
    repository.get_learned_words.return_value = 20

    mock_get_achievements.return_value = [ 
        "Achievement 1", 
        "Achievement 2", 
    ]

    service = ProfileService(repository)

    result = await service.get_achievements_text(user_id=123)

    assert "🏅 Достижения" in result
    assert "Achievement 1" in result
    assert "Achievement 2" in result

    mock_get_achievements.assert_called_once_with(
    10,
    100,
    20,
    )

    repository.get_statistics.assert_awaited_once_with(123)
    repository.get_xp.assert_awaited_once_with(123)
    repository.get_learned_words.assert_awaited_once_with(123)

@patch("services.profile_service.get_achievements")
async def test_get_achievements_text_xp_is_none(mock_get_achievements):
    repository = AsyncMock() 

    stats = {
            "translations": 10,
    }

    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = None
    repository.get_learned_words.return_value = 20

    mock_get_achievements.return_value = [ 
        "Achievement 1", 
        "Achievement 2", 
    ]

    service = ProfileService(repository)

    result = await service.get_achievements_text(user_id=123)

    assert "🏅 Достижения" in result 
    assert "Achievement 1" in result 
    assert "Achievement 2" in result

    mock_get_achievements.assert_called_once_with( 10, 0, 20, )   

@patch("services.profile_service.get_achievements")
async def test_get_achievements_text_learned_words_is_none(mock_get_achievements):
    repository = AsyncMock()

    stats = {
        "translations": 10,
    }
    
    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = 100
    repository.get_learned_words.return_value = None

    mock_get_achievements.return_value = [ 
        "Achievement 1", 
        "Achievement 2", 
    ]

    service = ProfileService(repository)

    result = await service.get_achievements_text(user_id=123)

    assert "🏅 Достижения" in result 
    assert "Achievement 1" in result 
    assert "Achievement 2" in result

    mock_get_achievements.assert_called_once_with( 10, 100, 0, )   

@patch("services.profile_service.get_achievements")
async def test_get_achievements_text_learned_words_is_invalid(mock_get_achievements):
    repository = AsyncMock()

    stats = {
        "translations": 10,
    }
    
    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = 100
    repository.get_learned_words.return_value = "invalid"

    mock_get_achievements.return_value = [ 
        "Achievement 1", 
        "Achievement 2", 
    ]

    service = ProfileService(repository)

    result = await service.get_achievements_text(user_id=123)

    assert "🏅 Достижения" in result 
    assert "Achievement 1" in result 
    assert "Achievement 2" in result

    mock_get_achievements.assert_called_once_with( 10, 100, 0,)


@patch("services.profile_service.get_achievements")
async def test_get_achievements_text_xp_is_invalid(mock_get_achievements):
    repository = AsyncMock()

    stats = {
        "translations": 10,
    }
    
    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = "invalid"
    repository.get_learned_words.return_value = 20

    mock_get_achievements.return_value = [ 
        "Achievement 1", 
        "Achievement 2", 
    ]

    service = ProfileService(repository)

    result = await service.get_achievements_text(user_id=123)

    assert "🏅 Достижения" in result 
    assert "Achievement 1" in result 
    assert "Achievement 2" in result

    mock_get_achievements.assert_called_once_with( 10, 0, 20,)

@patch("services.profile_service.get_achievements")
async def test_get_achievements_text_learned_words_is_string(mock_get_achievements):
    repository = AsyncMock()

    stats = {
        "translations": 10,
    }
    
    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = 100
    repository.get_learned_words.return_value = "20"

    mock_get_achievements.return_value = [ 
        "Achievement 1", 
        "Achievement 2", 
    ]

    service = ProfileService(repository)

    result = await service.get_achievements_text(user_id=123)

    assert "🏅 Достижения" in result 
    assert "Achievement 1" in result 
    assert "Achievement 2" in result

    mock_get_achievements.assert_called_once_with( 10, 100, 20,)


@patch("services.profile_service.get_achievements")
async def test_get_achievements_text_without_translations(mock_get_achievements):
    repository = AsyncMock()

    stats = {}
    
    repository.get_statistics.return_value = stats
    repository.get_xp.return_value = 100
    repository.get_learned_words.return_value = 20

    mock_get_achievements.return_value = [ 
        "Achievement 1", 
        "Achievement 2", 
    ]

    service = ProfileService(repository)

    result = await service.get_achievements_text(user_id=123)

    assert "🏅 Достижения" in result 
    assert "Achievement 1" in result 
    assert "Achievement 2" in result

    mock_get_achievements.assert_called_once_with( 0, 100, 20,)






        




        




        




        



        




        




        




        