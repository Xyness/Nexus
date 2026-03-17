from app.agent.state import AgentState
from app.core.llm import get_llm


def analyst_node(state: AgentState) -> dict:
    """Analyze sentiment and extract key facts."""
    try:
        llm = get_llm()
        summaries_text = "\n".join(f"- {s}" for s in state.get("summaries", []))
        prompt = (
            f"You are a financial analyst. Based on these research summaries about "
            f"'{state['topic']}', provide:\n"
            f"1. Overall sentiment: SENTIMENT: bullish/bearish/neutral\n"
            f"2. Sentiment score: SCORE: 0.0 to 1.0 (0=very bearish, 1=very bullish)\n"
            f"3. Key facts: KEY_FACTS: (one per line, prefixed with '- ')\n\n"
            f"Summaries:\n{summaries_text}"
        )
        response = llm.invoke([{"role": "user", "content": prompt}])
        content = response.content

        # Parse structured response
        sentiment = "neutral"
        sentiment_score = 0.5
        key_facts = []

        for line in content.split("\n"):
            line_lower = line.strip().lower()
            if line_lower.startswith("sentiment:"):
                val = line.split(":", 1)[1].strip().lower()
                if val in ("bullish", "bearish", "neutral"):
                    sentiment = val
            elif line_lower.startswith("score:"):
                try:
                    sentiment_score = float(line.split(":", 1)[1].strip())
                except ValueError:
                    pass
            elif line.strip().startswith("- "):
                key_facts.append(line.strip().lstrip("- "))

        return {
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "key_facts": key_facts,
        }
    except Exception as e:
        return {
            "sentiment": "neutral",
            "sentiment_score": 0.5,
            "key_facts": [],
            "errors": [f"Analyst error: {e}"],
        }
