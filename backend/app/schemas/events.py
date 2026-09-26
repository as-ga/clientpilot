from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

EventType = Literal[
    "agent_started",
    "thinking",
    "tool_selected",
    "tool_started",
    "tool_completed",
    "decision_made",
    "action_started",
    "action_completed",
    "agent_completed",
    "agent_error",
]


class AgentEvent(BaseModel):
    type: EventType
    message: str
    run_id: str | None = None
    tool: str | None = None
    status: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
