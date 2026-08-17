import logging
from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-5"

# Structured outputs: the API constrains the response to this schema, so the
# returned text is always valid JSON: no markdown fences, no repair parsing.
_ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "relevance_score": {
            "type": "number",
            "description": "How relevant to crypto/finance markets, from 0 to 10.",
        },
        "affected_assets": {
            "type": "array",
            "items": {"type": "string"},
            "description": 'Affected asset symbols, e.g. ["BTC", "ETH", "SPY"].',
        },
        "sentiment": {"type": "string", "enum": ["bullish", "bearish", "neutral"]},
        "urgency": {
            "type": "string",
            "enum": ["breaking", "important", "normal", "noise"],
        },
        "summary": {
            "type": "string",
            "description": "Brief 1-2 sentence summary of the market impact.",
        },
        "confidence": {
            "type": "number",
            "description": "Confidence in this analysis, from 0 to 1.",
        },
    },
    "required": [
        "relevance_score",
        "affected_assets",
        "sentiment",
        "urgency",
        "summary",
        "confidence",
    ],
    "additionalProperties": False,
}


class AsyncLLMClient:
    """Async wrapper around the Anthropic SDK for news analysis."""

    def __init__(self, api_key: str):
        self._client = AsyncAnthropic(api_key=api_key)

    async def create_message(self, prompt: str) -> str:
        """Send a prompt to the LLM and return the JSON text response."""
        response = await self._client.messages.create(
            model=MODEL,
            # Adaptive thinking is on by default and shares this budget with the
            # response text, so leave headroom above the size of the JSON itself.
            max_tokens=4096,
            # Scoring one headline is a short, scoped task, so low effort keeps
            # latency and cost down on a feed polled every few minutes.
            output_config={
                "effort": "low",
                "format": {"type": "json_schema", "schema": _ANALYSIS_SCHEMA},
            },
            messages=[{"role": "user", "content": prompt}],
        )

        if response.stop_reason == "max_tokens":
            logger.warning("Analysis hit max_tokens; JSON may be truncated")

        # content is a list of blocks (thinking blocks precede text), so pick
        # the text block rather than indexing into position 0.
        for block in response.content:
            if block.type == "text":
                return block.text

        logger.error("No text block in response (stop_reason=%s)", response.stop_reason)
        return ""
