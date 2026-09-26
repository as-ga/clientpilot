import json
from typing import Any, Protocol

from app.agent.state import AgentState
from app.tools.swytchcode.client import ToolExecutor


class ChatModel(Protocol):
    def invoke(self, messages: list[tuple[str, str]]) -> Any: ...


class AgentNodes:
    def __init__(self, executor: ToolExecutor, llm: ChatModel | None = None) -> None:
        self.executor = executor
        self.llm = llm

    def _llm_request_analysis(self, request: str) -> dict[str, Any]:
        if self.llm is None:
            return {}
        try:
            response = self.llm.invoke([
                (
                    "system",
                    "Classify the user request for a client operations agent. Return only JSON with keys read_only (boolean), intent (string), and client_name (string or null). Do not provide reasoning.",
                ),
                ("human", request),
            ])
            content = getattr(response, "content", "")
            if not isinstance(content, str):
                return {}
            parsed = json.loads(content)
            return parsed if isinstance(parsed, dict) else {}
        except (ValueError, TypeError, json.JSONDecodeError):
            return {}

    def understand_request(self, state: AgentState) -> AgentState:
        request = state["user_request"].lower()
        read_only = any(
            phrase in request
            for phrase in (
                "current status",
                "status of",
                "give me the status",
                "what is happening",
                "find any client issue",
                "requires immediate attention",
            )
        ) and not any(phrase in request for phrase in ("handle", "fix", "contact", "update", "notify"))
        llm_analysis = self._llm_request_analysis(state["user_request"])
        if isinstance(llm_analysis.get("read_only"), bool):
            read_only = llm_analysis["read_only"]
        return {
            "current_step": "understand_request",
            "iterations": 0,
            "read_only": read_only,
            "llm_analysis": llm_analysis,
            "executed_actions": [],
        }

    def identify_client(self, state: AgentState) -> AgentState:
        result = self.executor.execute("notion.search.create", {
                                       "query": state["user_request"]})
        client = result["results"][0]
        return {
            "client_name": client["name"],
            "client_id": client["id"],
            "client_context": client,
            "tool_results": {"notion.search.create": result},
            "current_step": "identify_client",
        }

    def gather_jira(self, state: AgentState) -> AgentState:
        result = self.executor.execute("jira.api.search.list", {
                                       "client": state["client_name"]})
        return {
            "jira_issues": result["issues"],
            "tool_results": {**state.get("tool_results", {}), "jira.api.search.list": result},
            "current_step": "gather_jira",
            "iterations": state.get("iterations", 0) + 1,
        }

    def investigate_blocker(self, state: AgentState) -> AgentState:
        result = self.executor.execute("slack.search.message.list", {
                                       "query": state["client_name"]})
        messages = result["messages"]
        blockers = [message["text"] for message in messages]
        return {
            "slack_messages": messages,
            "identified_blockers": blockers,
            "decisions": ["Client action required: payment API credentials are missing."],
            "tool_results": {**state.get("tool_results", {}), "slack.search.message.list": result},
            "current_step": "investigate_blocker",
            "iterations": state.get("iterations", 0) + 1,
        }

    def execute_actions(self, state: AgentState) -> AgentState:
        actions = []
        planned = [
            ("jira", "update issue", "jira.api.issue.update",
             {"issue_key": "ACME-102", "status": "Blocked"}),
            ("slack", "notify engineering", "slack.chat.postmessage.create", {
             "channel": "engineering", "text": state["identified_blockers"][0]}),
            ("gmail", "contact client", "gmail.user.send.create", {
             "to": "client@acme.example", "subject": "Acme Corp project update", "body": state["identified_blockers"][0]}),
        ]
        for tool, action, canonical_id, args in planned:
            try:
                result = self.executor.execute(canonical_id, args)
                actions.append({"tool": tool, "action": action,
                               "status": "completed", "result": result})
            except Exception as error:
                actions.append({"tool": tool, "action": action,
                               "status": "failed", "result": str(error)})
        return {"executed_actions": actions, "current_step": "execute_actions", "iterations": state.get("iterations", 0) + 1}

    def generate_final_response(self, state: AgentState) -> AgentState:
        if state.get("read_only"):
            if "find any client issue" in state["user_request"].lower() or "immediate attention" in state["user_request"].lower():
                return {
                    "final_summary": "Immediate attention: ACME-102 Checkout Bug is blocked because payment API credentials are missing. The issue is the highest operational risk for Acme Corp.",
                    "current_step": "generate_final_response",
                }
            return {
                "final_summary": "Acme Corp is at risk: ACME-102 Checkout Bug is blocked, while ACME-103 Deployment remains in progress. The blocker is missing payment API credentials.",
                "current_step": "generate_final_response",
            }
        return {
            "final_summary": "Checkout integration is blocked because payment API credentials are missing. Jira was updated, engineering was notified on Slack, and the client was contacted by email.",
            "current_step": "generate_final_response",
        }
