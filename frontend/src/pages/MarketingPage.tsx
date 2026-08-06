import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts'

interface MarketingData {
  total_spend: number
  total_impressions: number
  total_conversions: number
  avg_roi: number
  by_channel: { channel: string; spend: number; roi: number; conversions: number }[]
  campaigns: { campaign: string; spend: number; roi: number; conversions: number }[]
  trends: { month: string; spend: number; conversions: number; roi: number }[]
}

const COLORS = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899']

export default function MarketingPage() {
  const [data, setData] = useState<MarketingData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchMarketingData = async () => {
      try {
        setLoading(true)
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/api/marketing`)

        if (!response.ok) throw new Error('Failed to fetch marketing data')

        const marketingData = await response.json()
        setData(marketingData)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
        setData(null)
      } finally {
        setLoading(false)
      }
    }

    fetchMarketingData()
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
        <h3 className="font-semibold">Error loading marketing data</h3>
        <p className="text-sm">{error || 'No data available'}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-100">Marketing Analytics</h1>
        <p className="text-slate-400 mt-2">Campaign performance and ROI analysis</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Total Spend</div>
          <div className="text-3xl font-bold text-blue-400 mt-2">
            ${(data.total_spend / 1000).toFixed(0)}K
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Impressions</div>
          <div className="text-3xl font-bold text-purple-400 mt-2">
            {(data.total_impressions / 1000000).toFixed(1)}M
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Conversions</div>
          <div className="text-3xl font-bold text-green-400 mt-2">
            {data.total_conversions.toLocaleString()}
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-slate-400 text-sm font-medium">Avg ROI</div>
          <div className={`text-3xl font-bold mt-2 ${data.avg_roi > 0 ? 'text-green-400' : 'text-red-400'}`}>
            {data.avg_roi.toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* ROI by Channel */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">ROI by Channel</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.by_channel}>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="channel" stroke="#94A3B8" />
              <YAxis stroke="#94A3B8" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #475569' }}
                labelStyle={{ color: '#E2E8F0' }}
              />
              <Bar dataKey="roi" fill="#10B981" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Spend Trends */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Spend & Conversions Trend</h2>
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
                dataKey="spend"
                stroke="#3B82F6"
                yAxisId="left"
                name="Spend ($K)"
              />
              <Line
                type="monotone"
                dataKey="conversions"
                stroke="#10B981"
                yAxisId="right"
                name="Conversions"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Campaigns & Channels */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Campaigns */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Campaign Performance</h2>
          <div className="space-y-3">
            {data.campaigns.slice(0, 5).map((campaign, idx) => (
              <div key={idx} className="flex items-center justify-between border-b border-slate-700/30 pb-3">
                <div>
                  <p className="text-sm font-medium text-slate-100">{campaign.campaign}</p>
                  <p className="text-xs text-slate-500">${(campaign.spend / 1000).toFixed(0)}K spent</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold text-green-400">{campaign.roi.toFixed(1)}% ROI</p>
                  <p className="text-xs text-slate-400">{campaign.conversions} conversions</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Channel Distribution */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Spend by Channel</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={data.by_channel}
                dataKey="spend"
                nameKey="channel"
                cx="50%"
                cy="50%"
                outerRadius={100}
              >
                {data.by_channel.map((_, idx) => (
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
