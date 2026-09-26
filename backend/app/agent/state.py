from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    user_request: str
    read_only: bool
    llm_analysis: dict[str, Any]
    client_name: str | None
    client_id: str | None
    client_context: dict[str, Any]
    jira_issues: list[dict[str, Any]]
    gmail_messages: list[dict[str, Any]]
    slack_messages: list[dict[str, Any]]
    stripe_data: dict[str, Any] | None
    identified_blockers: list[str]
    risks: list[str]
    decisions: list[str]
    planned_actions: list[dict[str, Any]]
    executed_actions: list[dict[str, Any]]
    tool_results: dict[str, Any]
    current_step: str
    iterations: int
    errors: list[str]
    final_summary: str
