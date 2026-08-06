import { useState, useEffect } from 'react'
import { api } from '../services/api'
import KPICards from './KPICards'
import { SkeletonCard } from './Skeleton'

export default function Dashboard() {
  const [status, setStatus] = useState<any>(null)
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
      setError(err.message || 'Failed to fetch dashboard status')
      console.error('Dashboard Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      {/* System Status Section */}
      <section>
        <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
          <span>🎯</span> System Overview
        </h2>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => <SkeletonCard key={i} />)}
          </div>
        ) : error ? (
          <div className="bg-red-900/20 border border-red-700/50 rounded-lg p-4">
            <p className="text-red-200 text-sm">{error}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="kpi-card success">
              <p className="text-slate-400 text-sm">System Status</p>
              <p className="text-2xl font-bold text-white mt-2">{status?.app || 'N/A'}</p>
              <div className="mt-2 text-xs text-emerald-300">✓ Operational</div>
            </div>
            <div className="kpi-card">
              <p className="text-slate-400 text-sm">Version</p>
              <p className="text-2xl font-bold text-white mt-2">{status?.version || 'N/A'}</p>
              <div className="mt-2 text-xs text-slate-400">Latest</div>
            </div>
            <div className={`kpi-card ${status?.database === 'connected' ? 'success' : 'danger'}`}>
              <p className="text-slate-400 text-sm">PostgreSQL</p>
              <p className="text-2xl font-bold text-white mt-2">
                {status?.database === 'connected' ? '✓' : '✗'}
              </p>
              <div className={`mt-2 text-xs ${status?.database === 'connected' ? 'text-emerald-300' : 'text-red-300'}`}>
                {status?.database === 'connected' ? 'Connected' : 'Disconnected'}
              </div>
            </div>
            <div className={`kpi-card ${status?.duckdb === 'connected' ? 'success' : 'warning'}`}>
              <p className="text-slate-400 text-sm">DuckDB</p>
              <p className="text-2xl font-bold text-white mt-2">
                {status?.duckdb === 'connected' ? '✓' : '✗'}
              </p>
              <div className={`mt-2 text-xs ${status?.duckdb === 'connected' ? 'text-emerald-300' : 'text-amber-300'}`}>
                {status?.duckdb === 'connected' ? 'Ready' : 'Loading'}
              </div>
            </div>
          </div>
        )}
      </section>

      {/* KPI Section */}
      <section>
        <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
          <span>📊</span> Key Performance Indicators
        </h2>
        <KPICards />
      </section>

      {/* Feature Status Section */}
      {status?.features && (
        <section>
          <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
            <span>✨</span> Enabled Features
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(status.features).map(([key, enabled]: [string, any]) => (
              <div
                key={key}
                className={`card flex items-center gap-3 p-4 ${
                  enabled
                    ? 'border-emerald-700/50 bg-emerald-900/10'
                    : 'border-slate-700/30 bg-slate-700/10'
                }`}
              >
                <span className={`text-2xl ${enabled ? '✅' : '❌'}`} />
                <span className="capitalize text-sm font-medium">
                  {key.replace(/_/g, ' ')}
                </span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Quick Links Section */}
      <section>
        <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
          <span>🔗</span> Quick Links
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <a
            href={`http://localhost:8000/docs`}
            target="_blank"
            rel="noopener noreferrer"
            className="card hover:border-blue-500/50 p-4 cursor-pointer text-center"
          >
            <span className="text-3xl block mb-2">📚</span>
            <p className="font-semibold text-white text-sm">API Docs</p>
            <p className="text-xs text-slate-400 mt-1">Swagger UI</p>
          </a>
          <a
            href={`http://localhost:8000/health`}
            target="_blank"
            rel="noopener noreferrer"
            className="card hover:border-emerald-500/50 p-4 cursor-pointer text-center"
          >
            <span className="text-3xl block mb-2">🏥</span>
            <p className="font-semibold text-white text-sm">Health Check</p>
            <p className="text-xs text-slate-400 mt-1">System Status</p>
          </a>
          <a
            href={`http://localhost:8000`}
            target="_blank"
            rel="noopener noreferrer"
            className="card hover:border-purple-500/50 p-4 cursor-pointer text-center"
          >
            <span className="text-3xl block mb-2">🔌</span>
            <p className="font-semibold text-white text-sm">API Root</p>
            <p className="text-xs text-slate-400 mt-1">Base Endpoint</p>
          </a>
        </div>
      </section>
    </div>
  )
}
