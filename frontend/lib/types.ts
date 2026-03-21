export type Status = "APPROVED" | "NEEDS_INFO" | "BLOCKED" | "PENDING";
export type RouterAction = "retrieve" | "blocked";

export interface EvidenceChunk {
  id: string;
  source_doc: string;
  title: string;
  tags: string[];
  content: string;
}

export interface Answer {
  question_id: string;
  question_text: string;
  status: Status;
  draft_answer: string | null;
  citations: EvidenceChunk[];
  reason: string;
}

export interface FollowupTask {
  id: string;
  run_id: string;
  question_id: string;
  description: string;
  created_at: string;
}

export interface AuditEvent {
  id: string;
  run_id: string;
  question_id: string;
  agent: string;
  action: string;
  detail: string;
  created_at: string;
}

export interface RunResult {
  id: string;
  created_at: string;
  answers: Answer[];
  tasks: FollowupTask[];
  audit_events: AuditEvent[];
}

export interface DemoLoadResult {
  questions_loaded: number;
  evidence_loaded: number;
}
