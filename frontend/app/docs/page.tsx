import Link from "next/link";

export default function DocsPage() {
  return (
    <main className="min-h-screen bg-paper px-6 py-10 text-ink md:px-12">
      <div className="mx-auto max-w-4xl">
        <Link
          href="/"
          className="font-sans text-xs uppercase tracking-[0.25em] text-signal"
        >
          ClientPilot
        </Link>
        <h1 className="mt-10 text-5xl tracking-tight">
          How ClientPilot operates
        </h1>
        <p className="mt-5 max-w-2xl text-xl leading-relaxed text-ink/70">
          ClientPilot uses LangGraph to interpret a request, inspect the client
          through Swytchcode tools, identify blockers, and conditionally execute
          approved actions.
        </p>
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {[
            [
              "01",
              "Understand",
              "Classify the request and identify the relevant client.",
            ],
            [
              "02",
              "Investigate",
              "Gather only the context needed from connected business tools.",
            ],
            [
              "03",
              "Act",
              "Update systems, coordinate the team, and report what actually happened.",
            ],
          ].map(([number, title, description]) => (
            <section key={number} className="border-t border-ink/20 pt-4">
              <p className="font-sans text-xs font-bold tracking-widest text-signal">
                {number}
              </p>
              <h2 className="mt-4 text-2xl">{title}</h2>
              <p className="mt-3 font-sans text-sm leading-relaxed text-ink/65">
                {description}
              </p>
            </section>
          ))}
        </div>
      </div>
    </main>
  );
}
