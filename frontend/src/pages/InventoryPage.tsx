import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface InventoryData {
  total_value: number
  total_quantity: number
  low_stock_count: number
  turnover_rate: number
  by_product: { product: string; quantity: number; reorder_point: number; value: number; status: string }[]
  warehouse: { warehouse: string; total_items: number; value: number; utilization: number }[]
  by_category: { category: string; items: number; low_stock: number; value: number }[]
}

export default function InventoryPage() {
  const [data, setData] = useState<InventoryData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchInventoryData = async () => {
      try {
        setLoading(true)
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/api/inventory`)

        if (!response.ok) throw new Error('Failed to fetch inventory data')

        const inventoryData = await response.json()
        setData(inventoryData)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        setData(null)
      } finally {
        setLoading(false)
      }
    }

    fetchInventoryData()
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
        <h3 className="font-semibold">Error loading inventory data</h3>
        <p className="text-sm">{error || 'No data available'}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-100">Inventory Management</h1>
        <p className="text-slate-400 mt-2">Stock levels, warehouse status, and turnover metrics</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Total Value</div>
          <div className="text-3xl font-bold text-blue-400 mt-2">
            ${(data.total_value / 1000000).toFixed(2)}M
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Total Items</div>
          <div className="text-3xl font-bold text-green-400 mt-2">
            {data.total_quantity.toLocaleString()}
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className={`text-slate-400 text-sm font-medium ${data.low_stock_count > 0 ? 'text-red-400' : ''}`}>
            Low Stock Items
          </div>
          <div className={`text-3xl font-bold mt-2 ${data.low_stock_count > 0 ? 'text-red-400' : 'text-green-400'}`}>
            {data.low_stock_count}
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Turnover Rate</div>
          <div className="text-3xl font-bold text-purple-400 mt-2">
            {data.turnover_rate.toFixed(2)}x
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Stock Health by Category */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Stock Health by Category</h2>
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
              <Bar dataKey="items" fill="#3B82F6" radius={[8, 8, 0, 0]} name="Total Items" />
              <Bar dataKey="low_stock" fill="#EF4444" radius={[8, 8, 0, 0]} name="Low Stock" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Warehouse Utilization */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Warehouse Utilization</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.warehouse}>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="warehouse" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" label={{ value: 'Utilization %', angle: -90, position: 'insideLeft' }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #475569' }}
                labelStyle={{ color: '#E2E8F0' }}
              />
              <Bar dataKey="utilization" fill="#F59E0B" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Low Stock Alerts & Product List */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Low Stock Alerts */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">⚠️ Low Stock Alerts</h2>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {data.by_product
              .filter((p) => p.status === 'low')
              .map((product, idx) => (
                <div key={idx} className="bg-red-500/10 border border-red-500/30 rounded p-3">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-semibold text-slate-100">{product.product}</p>
                      <p className="text-xs text-slate-400">Reorder: {product.reorder_point} units</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-bold text-red-400">{product.quantity} units</p>
                      <p className="text-xs text-red-400">Below threshold</p>
                    </div>
                  </div>
                </div>
              ))}
            {data.by_product.filter((p) => p.status === 'low').length === 0 && (
              <p className="text-slate-400 text-center py-4">✅ No low stock items</p>
            )}
          </div>
        </div>

        {/* Top Products by Value */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Top Products by Value</h2>
          <div className="space-y-3">
            {data.by_product
              .sort((a, b) => b.value - a.value)
              .slice(0, 5)
              .map((product, idx) => (
                <div key={idx} className="flex items-center justify-between border-b border-slate-700/30 pb-3">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-slate-100">{product.product}</p>
                    <p className="text-xs text-slate-500">{product.quantity} units in stock</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold text-blue-400">
                      ${(product.value / 1000).toFixed(0)}K
                    </p>
                    <p className={`text-xs ${product.status === 'low' ? 'text-red-400' : 'text-green-400'}`}>
                      {product.status === 'low' ? '⚠️ Low' : '✅ OK'}
                    </p>
                  </div>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  )
}
