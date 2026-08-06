import { useState, useEffect } from 'react'

interface Recommendation {
  id: string
  title: string
  description: string
  impact: string
  priority: 'high' | 'medium' | 'low'
  effort: 'low' | 'medium' | 'high'
  expected_benefit: string
}

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        setLoading(true)
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/api/recommendations`)

        if (!response.ok) throw new Error('Failed to fetch recommendations')

        const data = await response.json()
        setRecommendations(Array.isArray(data) ? data : data.recommendations || [])
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        setRecommendations([])
      } finally {
        setLoading(false)
      }
    }

    fetchRecommendations()
  }, [])

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'text-red-400 bg-red-500/10 border-red-500/30'
      case 'medium':
        return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/30'
      case 'low':
        return 'text-blue-400 bg-blue-500/10 border-blue-500/30'
      default:
        return 'text-slate-400 bg-slate-500/10 border-slate-500/30'
    }
  }

  const getEffortColor = (effort: string) => {
    switch (effort) {
      case 'high':
        return 'bg-red-500/20'
      case 'medium':
        return 'bg-yellow-500/20'
      case 'low':
        return 'bg-green-500/20'
      default:
        return 'bg-slate-500/20'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-100">Recommendations</h1>
        <p className="text-slate-400 mt-2">AI-powered suggestions based on your data analysis</p>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-4 text-red-400">
          <h3 className="font-semibold">Error loading recommendations</h3>
          <p className="text-sm">{error}</p>
        </div>
      )}

      {recommendations.length === 0 && !error && (
        <div className="bg-blue-500/10 border border-blue-500/50 rounded-lg p-4 text-blue-400">
          <h3 className="font-semibold">No recommendations available</h3>
          <p className="text-sm">Run analytics queries in the chat to generate AI recommendations</p>
        </div>
      )}

      {/* Recommendations List */}
      <div className="grid grid-cols-1 gap-4">
        {recommendations.map((rec) => (
          <div
            key={rec.id}
            className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6 hover:border-slate-600/50 transition"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-slate-100">{rec.title}</h3>
                <p className="text-slate-400 mt-1">{rec.description}</p>
              </div>
              <div className={`ml-4 px-3 py-1 rounded-full border text-xs font-medium whitespace-nowrap ${getPriorityColor(rec.priority)}`}>
                {rec.priority.toUpperCase()}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="bg-slate-700/30 rounded p-3">
                <p className="text-slate-400 text-xs mb-1">Impact</p>
                <p className="text-sm font-semibold text-slate-100">{rec.impact}</p>
              </div>
              <div className={`rounded p-3 ${getEffortColor(rec.effort)}`}>
                <p className="text-slate-400 text-xs mb-1">Effort Required</p>
                <p className="text-sm font-semibold text-slate-100">{rec.effort.toUpperCase()}</p>
              </div>
              <div className="bg-green-500/10 border border-green-500/30 rounded p-3">
                <p className="text-slate-400 text-xs mb-1">Expected Benefit</p>
                <p className="text-sm font-semibold text-green-400">{rec.expected_benefit}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {recommendations.length > 0 && (
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-slate-100 mb-3">How to Use These Recommendations</h3>
          <ul className="space-y-2 text-slate-400 text-sm">
            <li>✓ Review each recommendation and its expected impact</li>
            <li>✓ Prioritize based on effort vs impact trade-off</li>
            <li>✓ Start with high-impact, low-effort recommendations</li>
            <li>✓ Implement in your organization</li>
            <li>✓ Monitor results and come back for updated recommendations</li>
          </ul>
        </div>
      )}
    </div>
  )
}
