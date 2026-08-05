import { useEffect, useState } from 'react'
import { api, Recommendation } from '../services/api'

interface RecommendationPanelProps {
  filters?: Record<string, any>
}

export default function RecommendationPanel({ filters }: RecommendationPanelProps) {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [expanded, setExpanded] = useState<string | null>(null)

  useEffect(() => {
    fetchRecommendations()
  }, [filters])

  const fetchRecommendations = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.getRecommendations(filters)
      setRecommendations(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch recommendations')
    } finally {
      setLoading(false)
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-50 dark:bg-red-900 border-red-200 dark:border-red-700'
      case 'medium':
        return 'bg-yellow-50 dark:bg-yellow-900 border-yellow-200 dark:border-yellow-700'
      case 'low':
        return 'bg-blue-50 dark:bg-blue-900 border-blue-200 dark:border-blue-700'
      default:
        return 'bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700'
    }
  }

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 dark:bg-red-800 text-red-800 dark:text-red-100'
      case 'medium':
        return 'bg-yellow-100 dark:bg-yellow-800 text-yellow-800 dark:text-yellow-100'
      case 'low':
        return 'bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-100'
      default:
        return 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-100'
    }
  }

  if (loading) {
    return <div className="text-center py-8 text-gray-500">Loading recommendations...</div>
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
        <p className="text-red-800 dark:text-red-100">Error: {error}</p>
      </div>
    )
  }

  if (recommendations.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No recommendations available yet.
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">💡 Recommendations</h3>
      <div className="space-y-3">
        {recommendations.map((rec) => (
          <div
            key={rec.id}
            className={`rounded-lg border p-4 cursor-pointer transition hover:shadow-md ${getPriorityColor(rec.priority)}`}
            onClick={() => setExpanded(expanded === rec.id ? null : rec.id)}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    {rec.title}
                  </h4>
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${getPriorityBadge(rec.priority)}`}>
                    {rec.priority.toUpperCase()}
                  </span>
                </div>
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  Impact: <span className="font-semibold">{rec.expected_impact}</span>
                </p>
              </div>
              <span className="text-xl ml-2">
                {expanded === rec.id ? '▼' : '▶'}
              </span>
            </div>

            {expanded === rec.id && (
              <div className="mt-4 pt-4 border-t border-gray-300/30 dark:border-gray-600/30 space-y-3">
                <p className="text-sm text-gray-800 dark:text-gray-200">
                  {rec.description}
                </p>

                {rec.department && (
                  <div>
                    <p className="text-xs text-gray-600 dark:text-gray-400 font-semibold">DEPARTMENT</p>
                    <p className="text-sm text-gray-900 dark:text-white">{rec.department}</p>
                  </div>
                )}

                {(rec.estimated_cost !== undefined || rec.estimated_savings !== undefined) && (
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    {rec.estimated_cost !== undefined && (
                      <div className="bg-white/50 dark:bg-white/5 rounded p-2">
                        <p className="text-gray-600 dark:text-gray-400 text-xs">Est. Cost</p>
                        <p className="font-semibold text-gray-900 dark:text-white">
                          ${rec.estimated_cost.toLocaleString()}
                        </p>
                      </div>
                    )}
                    {rec.estimated_savings !== undefined && (
                      <div className="bg-white/50 dark:bg-white/5 rounded p-2">
                        <p className="text-gray-600 dark:text-gray-400 text-xs">Est. Savings</p>
                        <p className="font-semibold text-green-600 dark:text-green-400">
                          ${rec.estimated_savings.toLocaleString()}
                        </p>
                      </div>
                    )}
                  </div>
                )}

                <button
                  className="mt-3 w-full px-3 py-2 bg-blue-600 text-white text-sm font-medium rounded hover:bg-blue-700 transition"
                  onClick={(e) => {
                    e.stopPropagation()
                    // TODO: Implement action handler
                  }}
                >
                  Take Action →
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
