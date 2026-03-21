import type { Answer } from "@/lib/types";
import { CitationsList } from "./CitationsList";
import { StatusBadge } from "./StatusBadge";

const BLOCKED_BG = "bg-red-50 border-red-200";
const DEFAULT_BG = "bg-white border-gray-200";

export function ResultsTable({ answers }: { answers: Answer[] }) {
  return (
    <section>
      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
        Answers
      </h2>
      <div className="space-y-3">
        {answers.map((answer) => {
          const isBlocked = answer.status === "BLOCKED";
          return (
            <div
              key={answer.question_id}
              className={`rounded-lg border p-4 ${isBlocked ? BLOCKED_BG : DEFAULT_BG}`}
            >
              <div className="flex items-start justify-between gap-3">
                <p className="text-sm font-medium text-gray-800 leading-snug">
                  {answer.question_text}
                </p>
                <div className="shrink-0">
                  <StatusBadge status={answer.status} />
                </div>
              </div>

              {answer.draft_answer && (
                <p className="mt-2 text-sm text-gray-700 leading-relaxed">
                  {answer.draft_answer}
                </p>
              )}

              {answer.reason && (
                <p
                  className={`mt-2 text-xs ${isBlocked ? "text-red-600 font-medium" : "text-gray-400"}`}
                >
                  {isBlocked ? "⚠ " : ""}
                  {answer.reason}
                </p>
              )}

              <CitationsList citations={answer.citations} />
            </div>
          );
        })}
      </div>
    </section>
  );
}
