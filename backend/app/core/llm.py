from app.config import get_settings


def get_llm():
    """Get LangChain chat model (for legacy report pipeline)."""
    settings = get_settings()
    if settings.mock_mode:
        from app.agent.mock import MockChatModel
        return MockChatModel()
    from langchain_anthropic import ChatAnthropic
    return ChatAnthropic(model="claude-sonnet-4-20250514", api_key=settings.anthropic_api_key)


def get_llm_client():
    """Get async LLM client for news analysis."""
    settings = get_settings()
    if settings.mock_mode:
        from app.agent.mock import MockLLMClient
        return MockLLMClient()
    from app.core.anthropic_client import AsyncLLMClient
    return AsyncLLMClient(api_key=settings.anthropic_api_key)
