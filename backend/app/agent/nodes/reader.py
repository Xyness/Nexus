from app.agent.state import AgentState
from app.core.llm import get_llm


def reader_node(state: AgentState) -> dict:
    """Filter and summarize search results."""
    try:
        results = state.get("search_results", [])
        if not results:
            return {"summaries": [], "errors": ["No search results to summarize"]}

        llm = get_llm()
        articles_text = "\n\n".join(
            f"**{r['title']}** ({r['url']})\n{r['content']}" for r in results
        )
        prompt = (
            f"You are a financial research reader. Summarize the key points from "
            f"these articles about '{state['topic']}'. Filter out irrelevant content. "
            f"Return concise bullet points.\n\n{articles_text}"
        )
        response = llm.invoke([{"role": "user", "content": prompt}])
        summaries = [
            s.strip().lstrip("- ")
            for s in response.content.strip().split("\n")
            if s.strip()
        ]
        return {"summaries": summaries}
    except Exception as e:
        return {"summaries": [], "errors": [f"Reader error: {e}"]}
