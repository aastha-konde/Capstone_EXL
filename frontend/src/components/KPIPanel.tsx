import { useEffect, useState } from 'react'
import { api, KPI } from '../services/api'

interface KPIPanelProps {
  sessionId?: string
  filters?: Record<string, any>
}

export default function KPIPanel({ sessionId, filters }: KPIPanelProps) {
  const [kpis, setKpis] = useState<KPI | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchKPIs()
  }, [sessionId, filters])

  const fetchKPIs = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.getKPIs(filters)
      setKpis(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch KPIs')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8 text-gray-500">Loading KPIs...</div>
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
        <p className="text-red-800 dark:text-red-100">Error: {error}</p>
      </div>
    )
  }

  if (!kpis || Object.keys(kpis).length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No KPI data available. Ask a question to generate analysis.
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Key Performance Indicators</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(kpis).slice(0, 6).map(([key, value]) => (
          <div
            key={key}
            className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 hover:shadow-md transition"
          >
            <p className="text-sm font-medium text-gray-600 dark:text-gray-400 capitalize">
              {key.replace(/_/g, ' ')}
            </p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
              {typeof value === 'number' ? value.toLocaleString(undefined, {
                maximumFractionDigits: 2,
              }) : String(value)}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}
