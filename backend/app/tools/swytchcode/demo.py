from typing import Any

CLIENT = {
    "id": "acme-corp",
    "name": "Acme Corp",
    "project": "E-commerce Platform",
    "deadline": "September 30",
    "account_manager": "Rahul",
}

ISSUES = [
    {"key": "ACME-101", "summary": "Payment Integration", "status": "Done"},
    {"key": "ACME-102", "summary": "Checkout Bug", "status": "Blocked"},
    {"key": "ACME-103", "summary": "Deployment", "status": "In Progress"},
]


def demo_execute(canonical_id: str, args: dict[str, Any]) -> dict[str, Any]:
    if canonical_id == "notion.search.create":
        return {"results": [CLIENT]}
    if canonical_id == "notion.page.get":
        return {"page": CLIENT}
    if canonical_id in {"jira.api.search.list", "jira.api.search.create"}:
        return {"issues": ISSUES}
    if canonical_id in {"jira.api.issue.get", "jira.api.issue.update"}:
        issue_key = args.get("issue_key", "ACME-102")
        issue = next(
            (item for item in ISSUES if item["key"] == issue_key), ISSUES[1])
        return {"issue": issue, "updated": canonical_id.endswith("update")}
    if canonical_id == "slack.search.message.list":
        return {"messages": [{"text": "Checkout is blocked because payment API credentials are missing."}]}
    if canonical_id == "slack.chat.postmessage.create":
        return {"sent": True, "channel": args.get("channel", "engineering")}
    if canonical_id == "gmail.user.send.create":
        return {"sent": True, "recipient": args.get("to", "client@acme.example")}
    raise ValueError(f"Demo tool is not configured: {canonical_id}")
