import type { Status } from "@/lib/types";

const STYLES: Record<Status, string> = {
  APPROVED: "bg-emerald-100 text-emerald-800 border border-emerald-200",
  NEEDS_INFO: "bg-amber-100 text-amber-800 border border-amber-200",
  BLOCKED: "bg-red-100 text-red-800 border border-red-200",
  PENDING: "bg-gray-100 text-gray-600 border border-gray-200",
};

const ICONS: Record<Status, string> = {
  APPROVED: "✓",
  NEEDS_INFO: "?",
  BLOCKED: "✕",
  PENDING: "…",
};

export function StatusBadge({ status }: { status: Status }) {
  return (
    <span
      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold ${STYLES[status]}`}
    >
      <span>{ICONS[status]}</span>
      {status.replace("_", " ")}
    </span>
  );
}
