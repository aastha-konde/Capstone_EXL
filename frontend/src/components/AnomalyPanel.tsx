import { useEffect, useState } from 'react'
import { api, Anomaly } from '../services/api'

interface AnomalyPanelProps {
  filters?: Record<string, any>
}

export default function AnomalyPanel({ filters }: AnomalyPanelProps) {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchAnomalies()
  }, [filters])

  const fetchAnomalies = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.getAnomalies(filters)
      setAnomalies(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch anomalies')
    } finally {
      setLoading(false)
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
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

  const getSeverityBadgeColor = (severity: string) => {
    switch (severity) {
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
    return <div className="text-center py-8 text-gray-500">Loading anomalies...</div>
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
        <p className="text-red-800 dark:text-red-100">Error: {error}</p>
      </div>
    )
  }

  if (anomalies.length === 0) {
    return (
      <div className="bg-green-50 dark:bg-green-900 border border-green-200 dark:border-green-700 rounded-lg p-4">
        <p className="text-green-800 dark:text-green-100">✓ No anomalies detected</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">⚠️ Anomalies Detected</h3>
      <div className="space-y-3">
        {anomalies.map((anomaly, idx) => (
          <div
            key={idx}
            className={`rounded-lg border p-4 ${getSeverityColor(anomaly.severity)}`}
          >
            <div className="flex items-start justify-between mb-2">
              <div>
                <p className="font-medium text-gray-900 dark:text-white capitalize">
                  {anomaly.metric.replace(/_/g, ' ')}
                </p>
                <p className="text-sm text-gray-700 dark:text-gray-300 mt-1">
                  {anomaly.description}
                </p>
              </div>
              <span className={`px-2 py-1 rounded text-xs font-semibold ${getSeverityBadgeColor(anomaly.severity)}`}>
                {anomaly.severity.toUpperCase()}
              </span>
            </div>

            <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
              <div className="bg-white/50 dark:bg-white/5 rounded p-2">
                <p className="text-gray-600 dark:text-gray-400 text-xs">Actual</p>
                <p className="font-semibold text-gray-900 dark:text-white">
                  {anomaly.value.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                </p>
              </div>
              <div className="bg-white/50 dark:bg-white/5 rounded p-2">
                <p className="text-gray-600 dark:text-gray-400 text-xs">Expected</p>
                <p className="font-semibold text-gray-900 dark:text-white">
                  {anomaly.expected.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
