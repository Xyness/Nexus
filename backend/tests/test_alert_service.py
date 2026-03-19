import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.agent.state import NewsAnalysisResult
from app.services.alert_service import should_alert


def _make_settings(threshold=7.0):
    s = MagicMock()
    s.alert_relevance_threshold = threshold
    return s


def _make_result(score=8.0, urgency="important", assets=None) -> NewsAnalysisResult:
    return NewsAnalysisResult(
        relevance_score=score,
        affected_assets=assets or ["BTC"],
        sentiment="bullish",
        urgency=urgency,
        summary="Test summary",
        confidence=0.8,
    )


@pytest.mark.asyncio
class TestShouldAlert:
    @patch("app.services.alert_service._is_on_cooldown", new_callable=AsyncMock, return_value=False)
    @patch("app.services.alert_service._get_watchlist_assets", new_callable=AsyncMock, return_value={})
    async def test_high_relevance_important_triggers_alert(self, mock_wl, mock_cd):
        result = _make_result(score=8.0, urgency="important")
        assert await should_alert(result, _make_settings()) is True

    @patch("app.services.alert_service._is_on_cooldown", new_callable=AsyncMock, return_value=False)
    @patch("app.services.alert_service._get_watchlist_assets", new_callable=AsyncMock, return_value={})
    async def test_high_relevance_breaking_triggers_alert(self, mock_wl, mock_cd):
        result = _make_result(score=9.0, urgency="breaking")
        assert await should_alert(result, _make_settings()) is True

    @patch("app.services.alert_service._is_on_cooldown", new_callable=AsyncMock, return_value=False)
    @patch("app.services.alert_service._get_watchlist_assets", new_callable=AsyncMock, return_value={})
    async def test_low_relevance_no_alert(self, mock_wl, mock_cd):
        result = _make_result(score=3.0, urgency="noise")
        assert await should_alert(result, _make_settings()) is False

    @patch("app.services.alert_service._is_on_cooldown", new_callable=AsyncMock, return_value=False)
    @patch("app.services.alert_service._get_watchlist_assets", new_callable=AsyncMock, return_value={})
    async def test_high_relevance_noise_no_alert(self, mock_wl, mock_cd):
        result = _make_result(score=8.0, urgency="noise")
        assert await should_alert(result, _make_settings()) is False

    @patch("app.services.alert_service._is_on_cooldown", new_callable=AsyncMock, return_value=True)
    @patch("app.services.alert_service._get_watchlist_assets", new_callable=AsyncMock, return_value={})
    async def test_cooldown_prevents_alert(self, mock_wl, mock_cd):
        result = _make_result(score=9.0, urgency="breaking")
        assert await should_alert(result, _make_settings()) is False

    @patch("app.services.alert_service._is_on_cooldown", new_callable=AsyncMock, return_value=False)
    @patch("app.services.alert_service._get_watchlist_assets", new_callable=AsyncMock, return_value={"BTC": 4.0})
    async def test_watchlist_lower_threshold(self, mock_wl, mock_cd):
        result = _make_result(score=5.0, urgency="normal", assets=["BTC"])
        assert await should_alert(result, _make_settings()) is True

    @patch("app.services.alert_service._is_on_cooldown", new_callable=AsyncMock, return_value=False)
    @patch("app.services.alert_service._get_watchlist_assets", new_callable=AsyncMock, return_value={"ETH": 6.0})
    async def test_watchlist_asset_not_matched(self, mock_wl, mock_cd):
        result = _make_result(score=5.0, urgency="normal", assets=["BTC"])
        assert await should_alert(result, _make_settings()) is False
