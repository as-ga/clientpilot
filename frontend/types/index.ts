export type AgentEvent = {
  type: string;
  message: string;
  run_id?: string;
  tool?: string;
  created_at?: string;
};

export type AgentRunResponse = {
  run_id: string;
  status: "queued" | "running" | "completed" | "failed";
};
