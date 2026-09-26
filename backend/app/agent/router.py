from app.agent.state import AgentState


def route_after_jira(state: AgentState) -> str:
    if state.get("read_only"):
        return "generate_final_response"
    if any(issue.get("status") == "Blocked" for issue in state.get("jira_issues", [])):
        return "investigate_blocker"
    return "generate_final_response"


def route_after_analysis(state: AgentState) -> str:
    if state.get("identified_blockers"):
        return "execute_actions"
    return "generate_final_response"
