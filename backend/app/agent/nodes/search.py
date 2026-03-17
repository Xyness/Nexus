from app.agent.state import AgentState
from app.core.search_client import get_search_client


def search_node(state: AgentState) -> dict:
    """Search for information on each sub-question."""
    try:
        client = get_search_client()
        all_results = []
        for question in state.get("sub_questions", [state["topic"]]):
            response = client.search(query=question, max_results=3)
            for r in response.get("results", []):
                all_results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", ""),
                    "query": question,
                })
        return {"search_results": all_results}
    except Exception as e:
        return {"errors": [f"Search error: {e}"]}
