export function LoadingState() {
  return (
    <div className="text-center py-20 text-gray-400">
      <div className="inline-block w-8 h-8 border-4 border-gray-200 border-t-gray-600 rounded-full animate-spin mb-4" />
      <p className="text-sm font-medium text-gray-500">
        Running agents — Router &rarr; Evidence &rarr; Policy…
      </p>
    </div>
  );
}
