import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Dashboard() {
  const [status, setStatus] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStatus()
  }, [])

  const fetchStatus = async () => {
    try {
      const response = await axios.get('http://localhost:8000/status')
      setStatus(response.data)
    } catch (err) {
      console.error('Failed to fetch status:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading dashboard...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
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

      {/* Quick Links */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          🔗 Quick Links
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="block p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition"
          >
            <p className="font-semibold text-blue-600 dark:text-blue-400">📚 API Docs</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Swagger UI</p>
          </a>
          <a
            href="http://localhost:8000/health"
            target="_blank"
            rel="noopener noreferrer"
            className="block p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition"
          >
            <p className="font-semibold text-blue-600 dark:text-blue-400">🏥 Health Check</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">System status</p>
          </a>
          <a
            href="http://localhost:8000/"
            target="_blank"
            rel="noopener noreferrer"
            className="block p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition"
          >
            <p className="font-semibold text-blue-600 dark:text-blue-400">🔌 API Root</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Base endpoint</p>
          </a>
        </div>
      </div>

      {/* Coming Soon */}
      <div className="bg-amber-50 dark:bg-amber-900 border border-amber-200 dark:border-amber-700 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-amber-900 dark:text-amber-100 mb-4">
          🚧 Coming Soon
        </h2>
        <ul className="space-y-2 text-amber-800 dark:text-amber-200">
          <li>• Interactive charts and visualizations</li>
          <li>• Real-time KPI monitoring</li>
          <li>• Anomaly detection alerts</li>
          <li>• Forecast trends</li>
          <li>• Recommendation engine</li>
          <li>• Custom report generation</li>
          <li>• Power BI Embedded integration</li>
        </ul>
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
  value: string
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
      <p className="text-2xl font-bold mt-2">{value}</p>
    </div>
  )
}
