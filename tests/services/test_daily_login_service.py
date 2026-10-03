
from unittest.mock import AsyncMock, patch

from services.daily_login_service import DailyLoginService
from utils.xp import DAILY_LOGIN_ACTION


@patch("services.daily_login_service.get_xp_reward")
async def test_process_daily_login_new_day(mock_get_xp_reward):
    repository = AsyncMock()

    repository.update_streak.return_value = (5, True)

    mock_get_xp_reward.return_value = 100

    service = DailyLoginService(repository)

    result = await service.process_daily_login(user_id=123)

    assert result["streak"] == 5
    assert result["xp"] == 100

    repository.update_daily_goal.assert_awaited_once_with(123)
    mock_get_xp_reward.assert_called_once_with(DAILY_LOGIN_ACTION)
    repository.add_xp.assert_awaited_once_with(123, 100)

async def test_process_daily_login_not_new_day():
    repository = AsyncMock()
    repository.update_streak.return_value = (5, False)

    service = DailyLoginService(repository)

    result = await service.process_daily_login(user_id=123)

    assert result is None

    repository.update_daily_goal.assert_awaited_once_with(123)
    repository.add_xp.assert_not_awaited()

     
