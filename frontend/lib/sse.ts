import type { AgentEvent } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export function subscribeToRun(
  runId: string,
  onEvent: (event: AgentEvent) => void,
  onError: () => void
) {
  const source = new EventSource(`${API_URL}/api/agent/stream/${runId}`);
  source.onmessage = (message) =>
    onEvent(JSON.parse(message.data) as AgentEvent);
  source.onerror = () => {
    source.close();
    onError();
  };
  return () => source.close();
}
