import { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts'

interface FinanceData {
  total_revenue: number
  total_cost: number
  total_profit: number
  profit_margin: number
  trends: { month: string; revenue: number; cost: number; profit: number }[]
  by_region: { region: string; revenue: number; cost: number; profit: number }[]
  by_category: { category: string; revenue: number; profit: number }[]
}

export default function FinancePage() {
  const [data, setData] = useState<FinanceData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchFinanceData = async () => {
      try {
        setLoading(true)
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/api/finance`)

        if (!response.ok) throw new Error('Failed to fetch finance data')

        const financeData = await response.json()
        setData(financeData)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        setData(null)
      } finally {
        setLoading(false)
      }
    }

    fetchFinanceData()
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
        <h3 className="font-semibold">Error loading finance data</h3>
        <p className="text-sm">{error || 'No data available'}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-100">Financial Analysis</h1>
        <p className="text-slate-400 mt-2">Revenue, costs, and profitability metrics</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Total Revenue</div>
          <div className="text-3xl font-bold text-blue-400 mt-2">
            ${(data.total_revenue / 1000000).toFixed(2)}M
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Total Cost</div>
          <div className="text-3xl font-bold text-orange-400 mt-2">
            ${(data.total_cost / 1000000).toFixed(2)}M
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Total Profit</div>
          <div className="text-3xl font-bold text-green-400 mt-2">
            ${(data.total_profit / 1000000).toFixed(2)}M
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Profit Margin</div>
          <div className="text-3xl font-bold text-purple-400 mt-2">
            {(data.profit_margin * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue vs Cost Trends */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Revenue vs Cost Trends</h2>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={data.trends}>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="month" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #475569' }}
                labelStyle={{ color: '#E2E8F0' }}
              />
              <Legend />
              <Area
                type="monotone"
                dataKey="revenue"
                fill="#3B82F6"
                stroke="#3B82F6"
                fillOpacity={0.6}
                name="Revenue"
              />
              <Area
                type="monotone"
                dataKey="cost"
                fill="#EF4444"
                stroke="#EF4444"
                fillOpacity={0.6}
                name="Cost"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Profit Trends */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Profit Trends</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data.trends}>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="month" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #475569' }}
                labelStyle={{ color: '#E2E8F0' }}
              />
              <Line
                type="monotone"
                dataKey="profit"
                stroke="#10B981"
                dot={{ fill: '#10B981' }}
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Regional & Category Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* By Region */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Financial Performance by Region</h2>
          <div className="space-y-4">
            {data.by_region.map((region, idx) => (
              <div key={idx} className="border border-slate-700/30 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <p className="font-semibold text-slate-100">{region.region}</p>
                  <p className="text-sm text-green-400 font-medium">
                    ${(region.profit / 1000).toFixed(0)}K profit
                  </p>
                </div>
                <div className="grid grid-cols-3 gap-2 text-xs">
                  <div>
                    <p className="text-slate-500">Revenue</p>
                    <p className="text-slate-100 font-semibold">${(region.revenue / 1000).toFixed(0)}K</p>
                  </div>
                  <div>
                    <p className="text-slate-500">Cost</p>
                    <p className="text-slate-100 font-semibold">${(region.cost / 1000).toFixed(0)}K</p>
                  </div>
                  <div>
                    <p className="text-slate-500">Margin</p>
                    <p className="text-slate-100 font-semibold">
                      {((region.profit / region.revenue) * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* By Category */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Profitability by Category</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.by_category}>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="category" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #475569' }}
                labelStyle={{ color: '#E2E8F0' }}
              />
              <Legend />
              <Bar dataKey="revenue" fill="#3B82F6" radius={[8, 8, 0, 0]} name="Revenue" />
              <Bar dataKey="profit" fill="#10B981" radius={[8, 8, 0, 0]} name="Profit" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
