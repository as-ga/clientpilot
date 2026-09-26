# ClientPilot Architecture

ClientPilot is an agentic operations loop, not a dashboard that calls every API in a fixed order. LangGraph owns conditional decisions, while Swytchcode is the only external integration execution boundary.

```mermaid
flowchart TD
    User --> Next[Next.js frontend]
    Next -->|POST run| API[FastAPI]
    API -->|background run| Graph[LangGraph state machine]
    Graph --> Understand[Understand request]
    Understand --> Identify[Identify client]
    Identify --> Context[Gather relevant context]
    Context --> Analyze[Analyze blocker state]
    Analyze --> Decision{Need action?}
    Decision -->|No| Final[Final response]
    Decision -->|Yes| Select[Select next tool]
    Select --> Swytchcode[Swytchcode runtime]
    Swytchcode --> Providers[Notion / Jira / Gmail / Slack / Stripe]
    Providers --> Analyze
    Final --> SSE[SSE event stream]
    SSE --> Next
    Graph --> DB[(PostgreSQL audit history)]
```

## Safety boundaries

- Provider HTTP requests are never constructed in ClientPilot.
- Only canonical tools enabled in Swytchcode `tooling.json` can execute in live mode.
- Demo mode uses the same executor interface with deterministic Acme Corp data.
- User-facing events contain workflow status only; hidden chain-of-thought is never streamed.
- Mutating actions are recorded with completed or failed status.
