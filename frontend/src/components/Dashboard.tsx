import { useEffect, useState } from 'react'
import { api, StatusResponse } from '../services/api'
import KPIPanel from './KPIPanel'
import TrendsPanel from './TrendsPanel'
import ForecastPanel from './ForecastPanel'
import AnomalyPanel from './AnomalyPanel'
import RecommendationPanel from './RecommendationPanel'

export default function Dashboard() {
  const [status, setStatus] = useState<StatusResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchStatus()
  }, [])

  const fetchStatus = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.getStatus()
      setStatus(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch status')
      console.error('Failed to fetch status:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8 text-gray-500">Loading dashboard...</div>
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
        <p className="text-red-800 dark:text-red-100">Error: {error}</p>
        <button
          onClick={fetchStatus}
          className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* System Status Cards */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">System Status</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatCard
            title="System Status"
            value={status?.app}
            icon="🚀"
          />
          <StatCard
            title="Version"
            value={status?.version}
            icon="📦"
          />
          <StatCard
            title="Database"
            value={status?.database}
            icon="💾"
            color={status?.database === 'connected' ? 'green' : 'red'}
          />
          <StatCard
            title="DuckDB"
            value={status?.duckdb}
            icon="⚡"
            color={status?.duckdb === 'connected' ? 'green' : 'red'}
          />
        </div>
      </div>

      {/* Features */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          🎯 Enabled Features
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {status?.features && Object.entries(status.features).map(([key, enabled]: [string, any]) => (
            <div key={key} className="flex items-center space-x-2">
              <span className={`text-2xl ${enabled ? '✅' : '❌'}`}></span>
              <span className="capitalize">{key.replace(/_/g, ' ')}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Analytics Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* KPI Panel */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <KPIPanel />
        </div>

        {/* Trends Panel */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <TrendsPanel />
        </div>
      </div>

      {/* Forecasts */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <ForecastPanel />
      </div>

      {/* Anomalies */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <AnomalyPanel />
      </div>

      {/* Recommendations */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <RecommendationPanel />
      </div>

      {/* Quick Links */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          🔗 Quick Links
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <LinkCard
            href={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/docs`}
            title="📚 API Docs"
            description="Swagger UI"
          />
          <LinkCard
            href={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/health`}
            title="🏥 Health Check"
            description="System status"
          />
          <LinkCard
            href={import.meta.env.VITE_API_URL || 'http://localhost:8000'}
            title="🔌 API Root"
            description="Base endpoint"
          />
        </div>
      </div>
    </div>
  )
}

function StatCard({
  title,
  value,
  icon,
  color = 'blue',
}: {
  title: string
  value?: string
  icon: string
  color?: string
}) {
  const colorClasses = {
    blue: 'bg-blue-50 dark:bg-blue-900 border-blue-200 dark:border-blue-700 text-blue-900 dark:text-blue-100',
    green: 'bg-green-50 dark:bg-green-900 border-green-200 dark:border-green-700 text-green-900 dark:text-green-100',
    red: 'bg-red-50 dark:bg-red-900 border-red-200 dark:border-red-700 text-red-900 dark:text-red-100',
  }

  return (
    <div className={`border rounded-lg p-6 ${colorClasses[color as keyof typeof colorClasses]}`}>
      <p className="text-4xl mb-2">{icon}</p>
      <p className="text-sm font-semibold opacity-75">{title}</p>
      <p className="text-2xl font-bold mt-2">{value || 'N/A'}</p>
    </div>
  )
}

function LinkCard({
  href,
  title,
  description,
}: {
  href: string
  title: string
  description: string
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="block p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition"
    >
      <p className="font-semibold text-blue-600 dark:text-blue-400">{title}</p>
      <p className="text-sm text-gray-600 dark:text-gray-400">{description}</p>
    </a>
  )
}
