import type { RunResult } from "@/lib/types";

interface SummaryCardsProps {
  run: RunResult;
}

export function SummaryCards({ run }: SummaryCardsProps) {
  const approved = run.answers.filter((a) => a.status === "APPROVED").length;
  const needsInfo = run.answers.filter((a) => a.status === "NEEDS_INFO").length;
  const blocked = run.answers.filter((a) => a.status === "BLOCKED").length;
  const tasks = run.tasks.length;

  const cards = [
    {
      label: "Approved",
      value: approved,
      color: "border-l-4 border-emerald-400",
      valueClass: "text-emerald-700",
    },
    {
      label: "Needs Info",
      value: needsInfo,
      color: "border-l-4 border-amber-400",
      valueClass: "text-amber-700",
    },
    {
      label: "Blocked",
      value: blocked,
      color: "border-l-4 border-red-400",
      valueClass: "text-red-700",
    },
    {
      label: "Follow-up Tasks",
      value: tasks,
      color: "border-l-4 border-blue-400",
      valueClass: "text-blue-700",
    },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
      {cards.map((card) => (
        <div
          key={card.label}
          className={`bg-white rounded-lg p-4 shadow-sm ${card.color}`}
        >
          <div className={`text-3xl font-bold ${card.valueClass}`}>
            {card.value}
          </div>
          <div className="text-sm text-gray-500 mt-1">{card.label}</div>
        </div>
      ))}
    </div>
  );
}
