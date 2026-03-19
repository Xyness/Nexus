import json
import logging

from app.agent.state import NewsAnalysisResult
from app.core.llm import get_llm_client

logger = logging.getLogger(__name__)

_ANALYSIS_PROMPT = """You are a financial news analyst. Analyze the following news item and return a JSON object with your analysis.

**News Title**: {title}
**Source**: {source}
**Content**: {content}

Return ONLY a valid JSON object with these fields:
- "relevance_score": float 0-10 (how relevant to crypto/finance markets)
- "affected_assets": list of affected asset symbols (e.g. ["BTC", "ETH", "SPY"])
- "sentiment": "bullish" | "bearish" | "neutral"
- "urgency": "breaking" | "important" | "normal" | "noise"
- "summary": brief 1-2 sentence summary of the market impact
- "confidence": float 0-1 (your confidence in this analysis)

JSON only, no markdown:"""


async def analyze_news_item(title: str, source: str, content: str) -> NewsAnalysisResult:
    """Analyze a news item and return structured analysis."""
    client = get_llm_client()
    prompt = _ANALYSIS_PROMPT.format(
        title=title,
        source=source,
        content=content[:3000],  # Limit content size
    )

    try:
        response = await client.create_message(prompt)
        # Parse JSON from response
        text = response.strip()
        # Handle potential markdown code blocks
        if text.startswith("```"):
            text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

        result = json.loads(text)

        return NewsAnalysisResult(
            relevance_score=float(result.get("relevance_score", 0)),
            affected_assets=result.get("affected_assets", []),
            sentiment=result.get("sentiment", "neutral"),
            urgency=result.get("urgency", "normal"),
            summary=result.get("summary", ""),
            confidence=float(result.get("confidence", 0.5)),
        )

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse analysis JSON: {e}")
        return NewsAnalysisResult(
            relevance_score=0,
            affected_assets=[],
            sentiment="neutral",
            urgency="noise",
            summary="Analysis failed: could not parse response",
            confidence=0,
        )
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return NewsAnalysisResult(
            relevance_score=0,
            affected_assets=[],
            sentiment="neutral",
            urgency="noise",
            summary=f"Analysis error: {str(e)[:100]}",
            confidence=0,
        )
