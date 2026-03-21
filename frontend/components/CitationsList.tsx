import type { EvidenceChunk } from "@/lib/types";

export function CitationsList({ citations }: { citations: EvidenceChunk[] }) {
  if (citations.length === 0) return null;

  return (
    <div className="mt-3">
      <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1.5">
        Citations
      </p>
      <ul className="flex flex-wrap gap-2">
        {citations.map((c) => (
          <li
            key={c.id}
            title={c.content}
            className="inline-flex items-center gap-1 px-2 py-1 bg-blue-50 border border-blue-100 rounded text-xs text-blue-700"
          >
            <span className="opacity-50">&#x1F4CE;</span>
            <span className="font-medium">{c.title}</span>
            <span className="opacity-50 text-blue-400">— {c.source_doc}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
