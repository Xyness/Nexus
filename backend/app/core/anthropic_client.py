import logging
from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)


class AsyncLLMClient:
    """Async wrapper around the Anthropic SDK for news analysis."""

    def __init__(self, api_key: str):
        self._client = AsyncAnthropic(api_key=api_key)

    async def create_message(self, prompt: str) -> str:
        """Send a prompt to the LLM and return the text response."""
        response = await self._client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
