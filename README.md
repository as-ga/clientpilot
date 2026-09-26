# ClientPilot

ClientPilot is an autonomous AI client operations manager for the Build with Swytchcode Gurgaon Edition buildathon, Track 6: AI Business Operator.

The system uses LangGraph to interpret an operations request, identify a client, gather context from relevant Swytchcode integrations, reason over blockers, conditionally execute approved actions, verify outcomes, and stream safe workflow events back to the UI.

## Current status

Phase 2 establishes the project structure and runtime contracts. Live integrations are intentionally not called directly: provider operations will be resolved from Swytchcode bundles and enabled through `.swytchcode/tooling.json`. `DEMO_MODE=true` will provide the local end-to-end path.

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