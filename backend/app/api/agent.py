import asyncio
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

from app.agent.graph import build_graph
from app.db.repository import Repository
from app.schemas.agent import AgentResult, AgentRunRequest, AgentRunResponse
from app.services.event_stream import stream

router = APIRouter(prefix="/api/agent", tags=["agent"])
_runs: dict[str, AgentResult] = {}
_run_ids: set[str] = set()
repository = Repository()


def event(run_id: str, event_type: str, message: str, **extra: str) -> None:
    stream.publish(
        run_id,
        {"type": event_type, "message": message, "run_id": run_id,
            "created_at": datetime.now(timezone.utc).isoformat(), **extra},
    )


async def execute_run(run_id: str, message: str) -> None:
    try:
        event(run_id, "agent_started", "ClientPilot started an operations run")
        event(run_id, "thinking", "Analyzing client context")
        event(run_id, "tool_started",
              "Finding the client in Notion", tool="notion")
        result = await asyncio.to_thread(build_graph().invoke, {"user_request": message})
        await asyncio.to_thread(
            repository.record_run,
            run_id,
            message,
            result.get("client_name"),
            "running",
        )
        event(run_id, "tool_completed", "Client context retrieved", tool="notion")
        event(run_id, "tool_completed", "Jira issues analyzed", tool="jira")
        if result.get("identified_blockers"):
            event(run_id, "decision_made", "Decision: client action required")
            event(run_id, "action_completed",
                  "Jira, Slack, and Gmail actions completed")
        final_result = AgentResult(
            run_id=run_id,
            client_name=result.get("client_name"),
            health="needs_attention" if result.get(
                "identified_blockers") else "healthy",
            summary=result.get("final_summary", "Client status analyzed."),
            blockers=result.get("identified_blockers", []),
            actions=[
                {"tool": item["tool"], "action": item["action"],
                    "status": item["status"],
                    "result_summary": "Action completed" if item["status"] == "completed" else str(item.get("result", "Action failed"))}
                for item in result.get("executed_actions", [])
            ],
        )
        _runs[run_id] = final_result
        await asyncio.to_thread(repository.complete_run, run_id, "completed", final_result.actions)
        event(run_id, "agent_completed", final_result.summary)
    except Exception as error:
        _runs[run_id] = AgentResult(
            run_id=run_id,
            health="unknown",
            summary=f"ClientPilot could not complete this run: {error}",
            blockers=[],
            actions=[],
        )
        await asyncio.to_thread(repository.complete_run, run_id, "failed", [])
        event(run_id, "agent_error", str(error))
    finally:
        stream.complete(run_id)


@router.post("/run", response_model=AgentRunResponse, status_code=202)
async def run_agent(request: AgentRunRequest) -> AgentRunResponse:
    run_id = str(uuid.uuid4())
    _run_ids.add(run_id)
    asyncio.create_task(execute_run(run_id, request.message))
    return AgentRunResponse(run_id=run_id, status="queued")


@router.get("/stream/{run_id}")
async def stream_agent(run_id: str) -> EventSourceResponse:
    if run_id not in _run_ids:
        raise HTTPException(status_code=404, detail="Run not found")
    return EventSourceResponse(stream.subscribe(run_id))


@router.get("/runs/{run_id}", response_model=AgentResult)
async def get_run(run_id: str) -> AgentResult:
    if run_id not in _runs:
        raise HTTPException(status_code=404, detail="Run not found")
    return _runs[run_id]
