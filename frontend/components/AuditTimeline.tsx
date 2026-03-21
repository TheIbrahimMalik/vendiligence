import type { AuditEvent } from "@/lib/types";

const AGENT_COLORS: Record<string, string> = {
  router: "bg-blue-500",
  evidence: "bg-purple-500",
  policy: "bg-emerald-500",
};

const BLOCKED_DOT = "bg-red-500";

function dotColor(event: AuditEvent): string {
  if (
    event.action.toLowerCase().includes("block") ||
    event.action.toLowerCase().includes("violation")
  ) {
    return BLOCKED_DOT;
  }
  return AGENT_COLORS[event.agent.toLowerCase()] ?? "bg-gray-400";
}

export function AuditTimeline({ events }: { events: AuditEvent[] }) {
  return (
    <section>
      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
        Audit Log
      </h2>
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <ul className="divide-y divide-gray-100">
          {events.map((event, i) => (
            <li key={event.id ?? i} className="flex items-start gap-3 px-4 py-3">
              <div className="mt-1.5 shrink-0">
                <span
                  className={`block w-2 h-2 rounded-full ${dotColor(event)}`}
                />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-xs font-semibold text-gray-600 uppercase">
                    {event.agent}
                  </span>
                  <span className="text-xs text-gray-400">/</span>
                  <span className="text-xs text-gray-700">{event.action}</span>
                  <span className="ml-auto text-xs text-gray-400 shrink-0">
                    {new Date(event.created_at).toLocaleTimeString()}
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-0.5 truncate">
                  {event.detail}
                </p>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
