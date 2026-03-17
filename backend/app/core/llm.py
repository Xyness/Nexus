from app.config import get_settings


def get_llm():
    settings = get_settings()
    if settings.mock_mode:
        from app.agent.mock import MockChatModel
        return MockChatModel()
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key)
