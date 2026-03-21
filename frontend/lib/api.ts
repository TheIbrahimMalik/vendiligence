import type { DemoLoadResult, RunResult } from "./types";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, options);
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

export async function loadDemoData(): Promise<DemoLoadResult> {
  return request<DemoLoadResult>("/api/demo/load", { method: "POST" });
}

export async function createRun(): Promise<RunResult> {
  return request<RunResult>("/api/runs", { method: "POST" });
}

export async function getRun(id: string): Promise<RunResult> {
  return request<RunResult>(`/api/runs/${id}`);
}
