export function EmptyState() {
  return (
    <div className="text-center py-20 text-gray-400">
      <div className="text-5xl mb-4">&#x1F4CB;</div>
      <p className="text-base font-medium text-gray-500">No run yet</p>
      <p className="text-sm mt-1">
        Load demo data, then click &ldquo;Run Questionnaire&rdquo; to start the
        agent pipeline.
      </p>
    </div>
  );
}
