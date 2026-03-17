from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes.planner import planner_node
from app.agent.nodes.search import search_node
from app.agent.nodes.reader import reader_node
from app.agent.nodes.analyst import analyst_node
from app.agent.nodes.writer import writer_node


def build_graph():
    """Build the linear agent pipeline: Planner → Search → Reader → Analyst → Writer."""
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("search", search_node)
    graph.add_node("reader", reader_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("writer", writer_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "search")
    graph.add_edge("search", "reader")
    graph.add_edge("reader", "analyst")
    graph.add_edge("analyst", "writer")
    graph.add_edge("writer", END)

    return graph.compile()


agent = build_graph()
