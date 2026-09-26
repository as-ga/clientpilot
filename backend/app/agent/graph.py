from langgraph.graph import END, START, StateGraph

from app.agent.nodes import AgentNodes
from app.agent.router import route_after_analysis, route_after_jira
from app.agent.state import AgentState
from app.config import get_settings
from app.llm import create_llm
from app.tools.swytchcode.client import SwytchcodeExecutor


def build_graph():
    settings = get_settings()
    llm = None
    if not settings.demo_mode and settings.llm_api_key:
        llm = create_llm(settings)
    nodes = AgentNodes(
        SwytchcodeExecutor(demo_mode=settings.demo_mode),
        llm=llm,
    )
    graph = StateGraph(AgentState)
    graph.add_node("understand_request", nodes.understand_request)
    graph.add_node("identify_client", nodes.identify_client)
    graph.add_node("gather_jira", nodes.gather_jira)
    graph.add_node("investigate_blocker", nodes.investigate_blocker)
    graph.add_node("execute_actions", nodes.execute_actions)
    graph.add_node("generate_final_response", nodes.generate_final_response)
    graph.add_edge(START, "understand_request")
    graph.add_edge("understand_request", "identify_client")
    graph.add_edge("identify_client", "gather_jira")
    graph.add_conditional_edges("gather_jira", route_after_jira)
    graph.add_conditional_edges("investigate_blocker", route_after_analysis)
    graph.add_edge("execute_actions", "generate_final_response")
    graph.add_edge("generate_final_response", END)
    return graph.compile()
