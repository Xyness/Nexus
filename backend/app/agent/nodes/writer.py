from app.agent.state import AgentState
from app.core.llm import get_llm


def writer_node(state: AgentState) -> dict:
    """Generate the final Markdown report."""
    try:
        llm = get_llm()
        facts = "\n".join(f"- {f}" for f in state.get("key_facts", []))
        summaries = "\n".join(f"- {s}" for s in state.get("summaries", []))
        prompt = (
            f"You are a professional financial report writer. Write a comprehensive "
            f"market intelligence report in Markdown format.\n\n"
            f"Topic: {state['topic']}\n"
            f"Sentiment: {state.get('sentiment', 'neutral')}\n"
            f"Sentiment Score: {state.get('sentiment_score', 0.5)}\n\n"
            f"Key Facts:\n{facts}\n\n"
            f"Research Summaries:\n{summaries}\n\n"
            f"Include: Executive Summary, Market Overview, Sentiment Analysis, "
            f"Key Developments, Risk Factors, and Outlook."
        )
        response = llm.invoke([{"role": "user", "content": prompt}])
        return {"report_md": response.content}
    except Exception as e:
        return {
            "report_md": f"# Error generating report\n\nAn error occurred: {e}",
            "errors": [f"Writer error: {e}"],
        }
