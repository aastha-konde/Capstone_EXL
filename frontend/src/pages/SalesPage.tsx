import { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

interface SalesData {
  total_revenue: number
  total_orders: number
  avg_order_value: number
  yoy_growth: number
  by_region: { region: string; revenue: number }[]
  by_product: { product: string; revenue: number; quantity: number }[]
  trends: { month: string; revenue: number; orders: number }[]
}

const COLORS = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899']

export default function SalesPage() {
  const [data, setData] = useState<SalesData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchSalesData = async () => {
      try {
        setLoading(true)
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/api/sales`)

        if (!response.ok) throw new Error('Failed to fetch sales data')

        const salesData = await response.json()
        setData(salesData)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        setData(null)
      } finally {
        setLoading(false)
      }
    }

    fetchSalesData()
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
        <h3 className="font-semibold">Error loading sales data</h3>
        <p className="text-sm">{error || 'No data available'}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-100">Sales Analytics</h1>
        <p className="text-slate-400 mt-2">Real-time sales performance and trends</p>
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
          <div className="text-slate-400 text-sm font-medium">Total Orders</div>
          <div className="text-3xl font-bold text-green-400 mt-2">
            {data.total_orders.toLocaleString()}
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Avg Order Value</div>
          <div className="text-3xl font-bold text-purple-400 mt-2">
            ${data.avg_order_value.toFixed(0)}
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">YoY Growth</div>
          <div className={`text-3xl font-bold mt-2 ${data.yoy_growth > 0 ? 'text-green-400' : 'text-red-400'}`}>
            {data.yoy_growth > 0 ? '+' : ''}{data.yoy_growth.toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue Trends */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Revenue Trends</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data.trends}>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="month" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #475569' }}
                labelStyle={{ color: '#E2E8F0' }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="revenue"
                stroke="#3B82F6"
                dot={{ fill: '#3B82F6' }}
                name="Revenue ($)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Sales by Region */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Sales by Region</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.by_region}>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="region" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #475569' }}
                labelStyle={{ color: '#E2E8F0' }}
              />
              <Bar dataKey="revenue" fill="#10B981" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Top Products & Regional Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Products */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Top Products</h2>
          <div className="space-y-3">
            {data.by_product.slice(0, 5).map((product, idx) => (
              <div key={idx} className="flex items-center justify-between">
                <div className="flex items-center gap-3 flex-1">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: COLORS[idx % COLORS.length] }}
                  ></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-slate-100">{product.product}</p>
                    <p className="text-xs text-slate-500">{product.quantity} units sold</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold text-slate-100">
                    ${(product.revenue / 1000).toFixed(0)}K
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Product Distribution Pie */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Product Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={data.by_product.slice(0, 5)}
                dataKey="revenue"
                nameKey="product"
                cx="50%"
                cy="50%"
                outerRadius={100}
              >
                {data.by_product.slice(0, 5).map((_, idx) => (
                  <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #475569' }}
                labelStyle={{ color: '#E2E8F0' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
