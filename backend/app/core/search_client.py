from app.config import get_settings


def get_search_client():
    settings = get_settings()
    if settings.mock_mode:
        from app.agent.mock import MockTavilyClient
        return MockTavilyClient()
    from tavily import TavilyClient
    return TavilyClient(api_key=settings.tavily_api_key)
