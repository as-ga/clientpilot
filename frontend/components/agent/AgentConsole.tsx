"use client";

import { FormEvent, useState } from "react";
import { ArrowUpRight, Check, CircleDot, LoaderCircle } from "lucide-react";

import { startAgent } from "@/lib/api";
import { subscribeToRun } from "@/lib/sse";
import type { AgentEvent } from "@/types";

const starter = "Check Acme Corp and handle anything blocking their project.";

export function AgentConsole() {
  const [message, setMessage] = useState(starter);
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [finalResult, setFinalResult] = useState<string | null>(null);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setRunning(true);
    setError(null);
    setEvents([]);
    setFinalResult(null);
    try {
      const run = await startAgent(message);
      subscribeToRun(
        run.run_id,
        (nextEvent) => {
          setEvents((current) => [...current, nextEvent]);
          if (nextEvent.type === "agent_completed")
            setFinalResult(nextEvent.message);
          if (
            nextEvent.type === "agent_completed" ||
            nextEvent.type === "agent_error"
          )
            setRunning(false);
        },
        () => {
          setRunning(false);
          setError("The event stream closed before the run completed.");
        }
      );
    } catch (requestError) {
      setRunning(false);
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to start run"
      );
    }
  }

  return (
    <main className="min-h-screen bg-paper px-6 py-8 text-ink md:px-12">
      <div className="mx-auto max-w-6xl">
        <header className="flex items-end justify-between border-b border-ink/15 pb-6">
          <div>
            <p className="mb-3 text-xs font-bold uppercase tracking-[0.3em] text-signal">
              ClientPilot / Agent desk
            </p>
            <h1 className="text-5xl leading-none tracking-tight md:text-7xl">
              Operational clarity,
              <br />
              without the handoff.
            </h1>
          </div>
          <span className="hidden rounded-full border border-moss/30 px-3 py-1 text-xs uppercase tracking-widest text-moss md:block">
            Demo mode
          </span>
        </header>

        <section className="grid gap-10 py-12 lg:grid-cols-[1.1fr_.9fr]">
          <form
            onSubmit={submit}
            className="border border-ink/15 bg-white/60 p-6 shadow-[10px_10px_0_#dbe0d5] md:p-8"
          >
            <div className="mb-10 flex items-center justify-between">
              <h2 className="text-2xl">Ask ClientPilot</h2>
              <CircleDot className="text-signal" size={20} />
            </div>
            <textarea
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              rows={5}
              className="w-full resize-none border-b border-ink/25 bg-transparent py-3 text-2xl outline-none placeholder:text-ink/35"
            />
            <button
              disabled={running || !message.trim()}
              className="mt-8 flex items-center gap-3 bg-ink px-5 py-3 font-sans text-sm font-bold uppercase tracking-widest text-paper transition hover:bg-signal disabled:cursor-not-allowed disabled:opacity-50"
            >
              {running ? (
                <LoaderCircle className="animate-spin" size={17} />
              ) : (
                <ArrowUpRight size={17} />
              )}
              {running ? "Running" : "Run agent"}
            </button>
            {error && (
              <p className="mt-4 font-sans text-sm text-signal">{error}</p>
            )}
          </form>

          <section className="border-t border-ink/15 pt-6">
            <div className="mb-8 flex items-center justify-between">
              <h2 className="text-2xl">Live activity</h2>
              <span className="font-sans text-xs uppercase tracking-widest text-ink/45">
                {events.length} events
              </span>
            </div>
            <div className="space-y-5">
              {events.length === 0 && (
                <p className="font-sans text-sm text-ink/50">
                  The agent workflow will appear here as it executes.
                </p>
              )}
              {events.map((item, index) => (
                <div
                  key={`${item.type}-${index}`}
                  className="flex gap-4 border-b border-ink/10 pb-4"
                >
                  <Check className="mt-1 shrink-0 text-moss" size={16} />
                  <div>
                    <p className="font-sans text-xs font-bold uppercase tracking-widest text-ink/45">
                      {item.type.replaceAll("_", " ")}
                    </p>
                    <p className="mt-1 text-lg">{item.message}</p>
                  </div>
                </div>
              ))}
            </div>
            {finalResult && (
              <div className="mt-10 border border-signal/35 bg-signal/10 p-5">
                <p className="font-sans text-xs font-bold uppercase tracking-widest text-signal">
                  Final result
                </p>
                <p className="mt-3 text-xl leading-relaxed">{finalResult}</p>
              </div>
            )}
          </section>
        </section>
      </div>
    </main>
  );
}
