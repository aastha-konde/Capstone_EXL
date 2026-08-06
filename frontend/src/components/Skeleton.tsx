export function SkeletonCard() {
  return (
    <div className="kpi-card animate-shimmer h-32 space-y-2">
      <div className="h-4 w-1/3 bg-slate-700 rounded" />
      <div className="h-8 w-1/2 bg-slate-700 rounded" />
      <div className="h-4 w-2/3 bg-slate-700 rounded" />
    </div>
  )
}

export function SkeletonChart() {
  return (
    <div className="chart-container animate-shimmer">
      <div className="space-y-4 h-full">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-12 bg-slate-700 rounded" />
        ))}
      </div>
    </div>
  )
}

export function SkeletonLine() {
  return <div className="h-4 bg-slate-700 rounded animate-shimmer" />
}

export function LoadingSpinner() {
  return (
    <div className="flex justify-center items-center">
      <div className="relative w-12 h-12">
        <div className="absolute inset-0 rounded-full border-4 border-slate-700" />
        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-500 animate-spin" />
      </div>
    </div>
  )
}

export function TypingIndicator() {
  return (
    <div className="flex gap-1 typing-indicator">
      <span className="w-2 h-2 bg-slate-500 rounded-full" />
      <span className="w-2 h-2 bg-slate-500 rounded-full" />
      <span className="w-2 h-2 bg-slate-500 rounded-full" />
    </div>
  )
}
