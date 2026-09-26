import type { AgentRunResponse } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function startAgent(message: string): Promise<AgentRunResponse> {
  const response = await fetch(`${API_URL}/api/agent/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!response.ok) throw new Error("Unable to start ClientPilot");
  return response.json();
}
