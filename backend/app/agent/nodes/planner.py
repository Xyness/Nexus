from app.agent.state import AgentState
from app.core.llm import get_llm


def planner_node(state: AgentState) -> dict:
    """Decompose the topic into sub-questions for research."""
    try:
        llm = get_llm()
        prompt = (
            f"You are a financial research planner. Decompose the following topic "
            f"into 3-5 specific sub-questions for thorough market research.\n\n"
            f"Topic: {state['topic']}\n\n"
            f"Return only the numbered sub-questions, one per line."
        )
        response = llm.invoke([{"role": "user", "content": prompt}])
        questions = [
            q.strip().lstrip("0123456789.-) ")
            for q in response.content.strip().split("\n")
            if q.strip()
        ]
        return {"sub_questions": questions}
    except Exception as e:
        return {
            "sub_questions": [state["topic"]],
            "errors": [f"Planner error: {e}"],
        }
