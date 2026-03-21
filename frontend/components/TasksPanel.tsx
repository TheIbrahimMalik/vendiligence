import type { FollowupTask } from "@/lib/types";

export function TasksPanel({ tasks }: { tasks: FollowupTask[] }) {
  if (tasks.length === 0) return null;

  return (
    <section>
      <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
        Follow-up Tasks
      </h2>
      <ul className="space-y-2">
        {tasks.map((task) => (
          <li
            key={task.id}
            className="flex items-start gap-3 bg-amber-50 border border-amber-100 rounded-lg px-4 py-3"
          >
            <span className="mt-0.5 text-amber-500 text-base">&#x25A1;</span>
            <div>
              <p className="text-sm text-gray-800">{task.description}</p>
              <p className="text-xs text-gray-400 mt-0.5">
                Question {task.question_id} &middot;{" "}
                {new Date(task.created_at).toLocaleTimeString()}
              </p>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
