import json
import pytest

from app.agent.mock import MockLLMClient
from app.agent.analyzer import analyze_news_item


@pytest.mark.asyncio
class TestMockLLMClient:
    async def test_returns_valid_json(self):
        client = MockLLMClient()
        response = await client.create_message("Analyze this news about Bitcoin")
        data = json.loads(response)

        assert "relevance_score" in data
        assert "affected_assets" in data
        assert "sentiment" in data
        assert "urgency" in data
        assert "summary" in data
        assert "confidence" in data

    async def test_relevance_score_range(self):
        client = MockLLMClient()
        for i in range(20):
            response = await client.create_message(f"Test prompt {i}")
            data = json.loads(response)
            assert 0 <= data["relevance_score"] <= 10

    async def test_sentiment_values(self):
        client = MockLLMClient()
        sentiments = set()
        for i in range(50):
            response = await client.create_message(f"Diverse prompt {i}")
            data = json.loads(response)
            sentiments.add(data["sentiment"])
        assert sentiments.issubset({"bullish", "bearish", "neutral"})

    async def test_urgency_values(self):
        client = MockLLMClient()
        urgencies = set()
        for i in range(50):
            response = await client.create_message(f"Various prompt {i}")
            data = json.loads(response)
            urgencies.add(data["urgency"])
        assert urgencies.issubset({"breaking", "important", "normal", "noise"})


@pytest.mark.asyncio
class TestAnalyzeNewsItem:
    async def test_analyze_returns_result(self):
        result = await analyze_news_item(
            title="Bitcoin Surges Past $100K",
            source="CoinDesk",
            content="Bitcoin has broken through the $100,000 barrier for the first time.",
        )
        assert "relevance_score" in result
        assert "sentiment" in result
        assert "urgency" in result
        assert "affected_assets" in result
        assert isinstance(result["affected_assets"], list)

    async def test_analyze_handles_empty_content(self):
        result = await analyze_news_item(
            title="Market Update",
            source="Reuters",
            content="",
        )
        assert "relevance_score" in result
