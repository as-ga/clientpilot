import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <h1 className="text-5xl font-bold">ClientPilot</h1>
      <p className="mt-4 text-lg text-gray-600">
        Autonomous client operations manager
      </p>
      <p className="mt-2 text-sm text-gray-500">
        Check Acme Corp and handle anything blocking their project.
      </p>
      <div className="mt-6 flex gap-4">
        <Link
          href="/agent"
          className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          Open Agent
        </Link>
        <Link
          href="/docs"
          className="rounded-md bg-gray-200 px-4 py-2 text-gray-800 hover:bg-gray-300"
        >
          Documentation
        </Link>
      </div>
    </main>
  );
}
