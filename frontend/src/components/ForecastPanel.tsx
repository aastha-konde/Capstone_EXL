import { useEffect, useState } from 'react'
import { api, Forecast } from '../services/api'

interface ForecastPanelProps {
  metric?: string
  filters?: Record<string, any>
}

export default function ForecastPanel({ metric, filters }: ForecastPanelProps) {
  const [forecasts, setForecasts] = useState<Forecast[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchForecasts()
  }, [metric, filters])

  const fetchForecasts = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.getForecasts(metric, filters)
      setForecasts(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch forecasts')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8 text-gray-500">Loading forecasts...</div>
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
        <p className="text-red-800 dark:text-red-100">Error: {error}</p>
      </div>
    )
  }

  if (forecasts.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No forecast data available.
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">📊 Forecasts</h3>
      <div className="space-y-3">
        {forecasts.map((forecast, idx) => {
          const ci = forecast.confidence_interval
          const lower = ci?.lower ?? 0
          const upper = ci?.upper ?? 0
          const range = upper - lower

          return (
            <div
              key={idx}
              className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4"
            >
              <div className="flex justify-between items-start mb-2">
                <div>
                  <p className="font-medium text-gray-900 dark:text-white capitalize">
                    {forecast.metric.replace(/_/g, ' ')}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    Period: {forecast.period} • Model: {forecast.model}
                  </p>
                </div>
                <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                  {typeof forecast.value === 'number'
                    ? forecast.value.toLocaleString(undefined, { maximumFractionDigits: 2 })
                    : forecast.value
                  }
                </p>
              </div>

              {ci && (
                <div className="mt-3">
                  <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400 mb-1">
                    <span>CI: {lower.toFixed(2)}</span>
                    <span>{upper.toFixed(2)}</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
                    <div
                      className="h-full bg-blue-500"
                      style={{
                        width: `${Math.min(100, (range / Math.abs(forecast.value || 1)) * 100)}%`,
                      }}
                    />
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
