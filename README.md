# ClientPilot

ClientPilot is an autonomous AI client operations manager for the Build with Swytchcode Gurgaon Edition buildathon, Track 6: AI Business Operator.

The system uses LangGraph to interpret an operations request, identify a client, gather context from relevant Swytchcode integrations, reason over blockers, conditionally execute approved actions, verify outcomes, and stream safe workflow events back to the UI.

## LLM configuration

The backend uses the OpenAI-compatible chat API contract. Configure only these variables:

```dotenv
LLM_URL=https://api.openai.com/v1
LLM_API_KEY=your-provider-key
LLM_MODEL=gpt-4o-mini
```

For Gemini, OpenRouter, Groq, Together, vLLM, or another compatible provider, set its documented compatible base URL and model ID. Native APIs with a different protocol need a separate provider adapter.

## Current status

Phase 2 establishes the project structure and runtime contracts. Live integrations are intentionally not called directly: provider operations will be resolved from Swytchcode bundles and enabled through `.swytchcode/tooling.json`. `DEMO_MODE=true` will provide the local end-to-end path.

The working prototype includes a conditional LangGraph loop, four-provider demo execution, SSE activity streaming, PostgreSQL persistence when configured, read-only scenarios, action-level failure reporting, and an in-app final result.

## Swytchcode live setup

Install and initialize Swytchcode in the repository:

```bash
npm install -g swytchcode
swytchcode init --editor=none --mode=sandbox --non-interactive
swytchcode login
swytchcode get notion
swytchcode get jira
swytchcode get gmail
swytchcode get slack
```

Inspect the downloaded methods before enabling them. The verified demo operation IDs are documented by each bundle; representative IDs are `notion.search.create`, `jira.api.search.list`, `jira.api.issue.update`, `slack.search.message.list`, `slack.chat.postmessage.create`, and `gmail.user.send.create`. Enable only the exact methods present in your fetched bundle with `swytchcode add <canonical-id>`.

Set `DEMO_MODE=false` only after the bundles, provider authentication, and enabled tools are ready. ClientPilot calls the Python `swytchcode-runtime` package; it does not call Notion, Jira, Slack, or Gmail directly.

## Demo scenarios

1. `Check Acme Corp and handle anything blocking their project.` gathers Notion and Jira context, investigates Slack conditionally, then updates Jira, notifies Slack, and emails the client.
2. `Give me the current status of Acme Corp.` gathers context and returns a status without mutations.
3. `Find any client issue that requires immediate attention.` identifies the blocked ACME-102 issue without performing actions.

## Run locally

```bash
cp .env.example .env
python3 -m venv backend/.venv
. backend/.venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload
```

The frontend will be added to the run instructions once its agent screen is connected to the API.

## Architecture

See [docs/architecture.md](docs/architecture.md). Swytchcode setup and verified provider operations are kept behind the backend adapter boundary; no provider endpoint is hardcoded here.