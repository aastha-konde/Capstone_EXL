import { useEffect, useState } from 'react'
import { api, Trend } from '../services/api'

interface TrendsPanelProps {
  filters?: Record<string, any>
}

export default function TrendsPanel({ filters }: TrendsPanelProps) {
  const [trends, setTrends] = useState<Trend[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await api.getAnalytics(undefined, filters)
        if (data?.trends) {
          setTrends(data.trends)
        }
      } catch (err: any) {
        setError(err.response?.data?.detail || err.message || 'Failed to fetch trends')
      } finally {
        setLoading(false)
      }
    }

    fetchAnalytics()
  }, [filters])

  const getTrendIcon = (direction: string) => {
    switch (direction) {
      case 'up':
        return '📈'
      case 'down':
        return '📉'
      case 'stable':
        return '➡️'
      default:
        return '➖'
    }
  }

  const getTrendColor = (direction: string) => {
    switch (direction) {
      case 'up':
        return 'text-green-600 dark:text-green-400'
      case 'down':
        return 'text-red-600 dark:text-red-400'
      case 'stable':
        return 'text-gray-600 dark:text-gray-400'
      default:
        return 'text-gray-600 dark:text-gray-400'
    }
  }

  if (loading) {
    return <div className="text-center py-8 text-gray-500">Loading trends...</div>
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
        <p className="text-red-800 dark:text-red-100">Error: {error}</p>
      </div>
    )
  }

  if (trends.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No trend data available.
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">📊 Trends</h3>
      <div className="space-y-3">
        {trends.map((trend, idx) => (
          <div
            key={idx}
            className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4"
          >
            <div className="flex items-center justify-between mb-2">
              <div>
                <p className="font-medium text-gray-900 dark:text-white capitalize">
                  {trend.metric.replace(/_/g, ' ')}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  Period: {trend.period}
                </p>
              </div>
              <span className={`text-2xl ${getTrendColor(trend.direction)}`}>
                {getTrendIcon(trend.direction)}
              </span>
            </div>

            <div className="flex items-center justify-between mt-3">
              <div className="flex-1">
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div
                    className={`h-full rounded-full ${
                      trend.direction === 'up'
                        ? 'bg-green-500'
                        : trend.direction === 'down'
                        ? 'bg-red-500'
                        : 'bg-gray-500'
                    }`}
                    style={{
                      width: `${Math.min(100, Math.abs(trend.percentage))}%`,
                    }}
                  />
                </div>
              </div>
              <span className={`ml-3 font-semibold text-sm ${getTrendColor(trend.direction)}`}>
                {trend.direction === 'up' ? '+' : ''}
                {trend.percentage.toFixed(1)}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
