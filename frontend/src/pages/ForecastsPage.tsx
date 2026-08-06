import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts'

interface ForecastData {
  revenue_forecast: Array<{ period: string; actual: number; forecast: number; upper_ci: number; lower_ci: number }>
  demand_forecast: Array<{ period: string; actual: number; forecast: number; upper_ci: number; lower_ci: number }>
  confidence: number
  model_type: string
  metrics: { mape: number; mae: number; rmse: number }
}

export default function ForecastsPage() {
  const [data, setData] = useState<ForecastData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchForecasts = async () => {
      try {
        setLoading(true)
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/api/forecasts`)

        if (!response.ok) throw new Error('Failed to fetch forecast data')

        const forecastData = await response.json()
        setData(forecastData)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        setData(null)
      } finally {
        setLoading(false)
      }
    }

    fetchForecasts()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-4 text-red-400">
        <h3 className="font-semibold">Error loading forecast data</h3>
        <p className="text-sm">{error || 'No data available'}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-100">Forecasts & Predictions</h1>
        <p className="text-slate-400 mt-2">ML-powered revenue and demand forecasts with confidence intervals</p>
      </div>

      {/* Model Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Forecast Model</div>
          <div className="text-2xl font-bold text-blue-400 mt-2">{data.model_type}</div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Confidence Level</div>
          <div className="text-2xl font-bold text-green-400 mt-2">{(data.confidence * 100).toFixed(0)}%</div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">MAPE Error</div>
          <div className="text-2xl font-bold text-purple-400 mt-2">{data.metrics.mape.toFixed(2)}%</div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">RMSE</div>
          <div className="text-2xl font-bold text-orange-400 mt-2">{data.metrics.rmse.toFixed(0)}</div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue Forecast */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Revenue Forecast</h2>
          <ResponsiveContainer width="100%" height={350}>
            <AreaChart data={data.revenue_forecast}>
              <defs>
                <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="colorCI" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#94A3B8" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#94A3B8" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="period" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #475569' }}
                labelStyle={{ color: '#E2E8F0' }}
              />
              <Legend />
              <Area
                type="monotone"
                dataKey="upper_ci"
                fill="url(#colorCI)"
                stroke="#94A3B8"
                strokeDasharray="5 5"
                name="Upper CI"
              />
              <Area
                type="monotone"
                dataKey="forecast"
                fill="url(#colorForecast)"
                stroke="#3B82F6"
                strokeWidth={2}
                name="Forecast"
              />
              <Area
                type="monotone"
                dataKey="lower_ci"
                fill="url(#colorCI)"
                stroke="#94A3B8"
                strokeDasharray="5 5"
                name="Lower CI"
              />
              <Line type="monotone" dataKey="actual" stroke="#10B981" strokeWidth={2} name="Actual" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Demand Forecast */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Demand Forecast</h2>
          <ResponsiveContainer width="100%" height={350}>
            <AreaChart data={data.demand_forecast}>
              <defs>
                <linearGradient id="colorDemand" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="period" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #475569' }}
                labelStyle={{ color: '#E2E8F0' }}
              />
              <Legend />
              <Area
                type="monotone"
                dataKey="upper_ci"
                fill="#94A3B8"
                stroke="#94A3B8"
                strokeDasharray="5 5"
                name="Upper CI"
                fillOpacity={0.2}
              />
              <Area
                type="monotone"
                dataKey="forecast"
                fill="url(#colorDemand)"
                stroke="#10B981"
                strokeWidth={2}
                name="Forecast"
              />
              <Area
                type="monotone"
                dataKey="lower_ci"
                fill="#94A3B8"
                stroke="#94A3B8"
                strokeDasharray="5 5"
                name="Lower CI"
                fillOpacity={0.2}
              />
              <Line type="monotone" dataKey="actual" stroke="#3B82F6" strokeWidth={2} name="Actual" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Model Info */}
      <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-slate-100 mb-4">Model Performance Metrics</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-700/30 rounded-lg p-4">
            <p className="text-slate-400 text-sm mb-2">Mean Absolute Percentage Error</p>
            <p className="text-2xl font-bold text-blue-400">{data.metrics.mape.toFixed(2)}%</p>
            <p className="text-xs text-slate-500 mt-1">Lower is better (lower error)</p>
          </div>
          <div className="bg-slate-700/30 rounded-lg p-4">
            <p className="text-slate-400 text-sm mb-2">Mean Absolute Error</p>
            <p className="text-2xl font-bold text-green-400">{data.metrics.mae.toFixed(0)}</p>
            <p className="text-xs text-slate-500 mt-1">Average absolute deviation</p>
          </div>
          <div className="bg-slate-700/30 rounded-lg p-4">
            <p className="text-slate-400 text-sm mb-2">Root Mean Squared Error</p>
            <p className="text-2xl font-bold text-purple-400">{data.metrics.rmse.toFixed(0)}</p>
            <p className="text-xs text-slate-500 mt-1">Penalizes larger errors more</p>
          </div>
        </div>
      </div>

      {/* Info Box */}
      <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
        <p className="text-sm text-blue-300">
          <strong>ℹ️ About These Forecasts:</strong> These predictions are generated using machine learning models
          (Prophet/ARIMA) trained on historical data. The confidence intervals show the range of uncertainty in the
          predictions. These are automatically updated as new data arrives.
        </p>
      </div>
    </div>
  )
}
