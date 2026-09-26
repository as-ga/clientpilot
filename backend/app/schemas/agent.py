from typing import Literal

from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class AgentRunResponse(BaseModel):
    run_id: str
    status: Literal["queued", "running", "completed", "failed"]


class ActionSummary(BaseModel):
    tool: str
    action: str
    status: Literal["planned", "completed", "failed"]
    result_summary: str


class AgentResult(BaseModel):
    run_id: str
    client_name: str | None = None
    health: str
    summary: str
    blockers: list[str] = []
    actions: list[ActionSummary] = []
