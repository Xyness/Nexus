import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone

from app.alerts.telegram import format_alert_message


class TestFormatAlertMessage:
    def _make_analysis(self, **kwargs):
        analysis = MagicMock()
        analysis.urgency = kwargs.get("urgency", "important")
        analysis.sentiment = kwargs.get("sentiment", "bullish")
        analysis.relevance_score = kwargs.get("relevance_score", 8.5)
        analysis.affected_assets = kwargs.get("affected_assets", ["BTC", "ETH"])
        analysis.summary = kwargs.get("summary", "Bitcoin surges on strong ETF inflows.")
        return analysis

    def _make_news_item(self, **kwargs):
        item = MagicMock()
        item.title = kwargs.get("title", "Bitcoin Breaks $100K")
        item.url = kwargs.get("url", "https://example.com/btc-100k")
        item.source = kwargs.get("source", "CoinDesk")
        item.fetched_at = kwargs.get("fetched_at", datetime.now(timezone.utc))
        return item

    def test_contains_title(self):
        msg = format_alert_message(self._make_analysis(), self._make_news_item())
        assert "Bitcoin Breaks $100K" in msg

    def test_contains_sentiment(self):
        msg = format_alert_message(self._make_analysis(), self._make_news_item())
        assert "bullish" in msg

    def test_contains_relevance_score(self):
        msg = format_alert_message(self._make_analysis(), self._make_news_item())
        assert "8.5/10" in msg

    def test_contains_assets(self):
        msg = format_alert_message(self._make_analysis(), self._make_news_item())
        assert "BTC" in msg
        assert "ETH" in msg

    def test_contains_url(self):
        msg = format_alert_message(self._make_analysis(), self._make_news_item())
        assert "https://example.com/btc-100k" in msg

    def test_contains_urgency(self):
        msg = format_alert_message(
            self._make_analysis(urgency="breaking"),
            self._make_news_item(),
        )
        assert "BREAKING" in msg

    def test_contains_summary(self):
        msg = format_alert_message(self._make_analysis(), self._make_news_item())
        assert "Bitcoin surges on strong ETF inflows" in msg
