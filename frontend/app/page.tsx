"use client";

import { useState } from "react";

import { ActionBar } from "@/components/ActionBar";
import { AuditTimeline } from "@/components/AuditTimeline";
import { DemoHeader } from "@/components/DemoHeader";
import { EmptyState } from "@/components/EmptyState";
import { LoadingState } from "@/components/LoadingState";
import { ResultsTable } from "@/components/ResultsTable";
import { SummaryCards } from "@/components/SummaryCards";
import { TasksPanel } from "@/components/TasksPanel";
import { createRun, loadDemoData } from "@/lib/api";
import type { RunResult } from "@/lib/types";

type LoadingState = "idle" | "loading-demo" | "running";

export default function Home() {
  const [loadingState, setLoadingState] = useState<LoadingState>("idle");
  const [demoLoaded, setDemoLoaded] = useState(false);
  const [run, setRun] = useState<RunResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleLoadDemo() {
    setLoadingState("loading-demo");
    setError(null);
    try {
      await loadDemoData();
      setDemoLoaded(true);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load demo data");
    } finally {
      setLoadingState("idle");
    }
  }

  async function handleRunQuestionnaire() {
    setLoadingState("running");
    setError(null);
    setRun(null);
    try {
      const result = await createRun();
      setRun(result);
    } catch (e) {
      setError(
        e instanceof Error ? e.message : "Agent pipeline failed — check backend"
      );
    } finally {
      setLoadingState("idle");
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <DemoHeader />

      <main className="max-w-5xl mx-auto px-4 py-6 space-y-6">
        {/* Action bar */}
        <ActionBar
          loadingState={loadingState}
          demoLoaded={demoLoaded}
          onLoadDemo={handleLoadDemo}
          onRunQuestionnaire={handleRunQuestionnaire}
        />

        {/* Error banner */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 text-sm text-red-700">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Run ID */}
        {run && (
          <p className="text-xs text-gray-400">
            Run ID: <code className="font-mono">{run.id}</code> &middot;{" "}
            {new Date(run.created_at).toLocaleString()}
          </p>
        )}

        {/* Summary cards */}
        {run && <SummaryCards run={run} />}

        {/* Main content */}
        {loadingState === "running" ? (
          <LoadingState />
        ) : run ? (
          <div className="space-y-6">
            <ResultsTable answers={run.answers} />
            <TasksPanel tasks={run.tasks} />
            <AuditTimeline events={run.audit_events} />
          </div>
        ) : (
          !error && <EmptyState />
        )}
      </main>
    </div>
  );
}
