"use client";

type LoadingState = "idle" | "loading-demo" | "running";

interface ActionBarProps {
  loadingState: LoadingState;
  demoLoaded: boolean;
  onLoadDemo: () => void;
  onRunQuestionnaire: () => void;
}

export function ActionBar({
  loadingState,
  demoLoaded,
  onLoadDemo,
  onRunQuestionnaire,
}: ActionBarProps) {
  const busy = loadingState !== "idle";

  return (
    <div className="flex items-center gap-3 flex-wrap">
      <button
        onClick={onLoadDemo}
        disabled={busy}
        className="px-4 py-2 rounded-md text-sm font-medium bg-gray-100 text-gray-700 border border-gray-300 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {loadingState === "loading-demo" ? "Loading…" : "Load Demo Data"}
      </button>

      {demoLoaded && (
        <span className="text-xs text-emerald-600 font-medium">
          ✓ Demo data loaded
        </span>
      )}

      <button
        onClick={onRunQuestionnaire}
        disabled={busy || !demoLoaded}
        className="px-4 py-2 rounded-md text-sm font-medium bg-gray-900 text-white hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {loadingState === "running" ? "Running agents…" : "Run Questionnaire"}
      </button>

      {!demoLoaded && loadingState === "idle" && (
        <span className="text-xs text-gray-400">
          Load demo data first to enable the run
        </span>
      )}
    </div>
  );
}
