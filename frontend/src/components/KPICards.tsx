import { useState, useEffect } from 'react'
import { api } from '../services/api'
import { SkeletonCard } from './Skeleton'

interface KPICardProps {
  title: string
  value: string | number
  trend?: number
  status?: 'success' | 'warning' | 'danger'
  icon?: string
  sparkline?: number[]
}

function KPICard({ title, value, trend, status = 'success', icon, sparkline }: KPICardProps) {
  const trendColor = trend === undefined ? 'text-slate-400' : trend > 0 ? 'text-emerald-400' : 'text-red-400'
  const trendIcon = trend === undefined ? '' : trend > 0 ? '📈' : '📉'

  return (
    <div className={`kpi-card ${status}`}>
      <div className="flex justify-between items-start mb-4">
        <div>
          <p className="text-slate-400 text-sm font-medium">{title}</p>
          <p className="text-3xl font-bold text-white mt-2">
            {typeof value === 'number' ? value.toLocaleString(undefined, { maximumFractionDigits: 1 }) : value}
          </p>
        </div>
        {icon && <span className="text-3xl">{icon}</span>}
      </div>

      {trend !== undefined && (
        <div className={`flex items-center gap-1 ${trendColor} text-sm font-semibold`}>
          <span>{trendIcon}</span>
          <span>{Math.abs(trend)}% {trend > 0 ? 'increase' : 'decrease'}</span>
        </div>
      )}

      {sparkline && (
        <div className="mt-4 h-12 flex items-end gap-1 opacity-50">
          {sparkline.map((v, i) => (
            <div
              key={i}
              className="flex-1 bg-blue-500 rounded-t opacity-70"
              style={{ height: `${(v / Math.max(...sparkline)) * 100}%` }}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export default function KPICards() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchKPIs()
  }, [])

  const fetchKPIs = async () => {
    try {
      setLoading(true)
      setError(null)
      await api.getKPIs()
    } catch (err: any) {
      setError(err.message || 'Failed to fetch KPIs')
      console.error('KPI Fetch Error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => <SkeletonCard key={i} />)}
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-900/20 border border-red-700/50 rounded-lg p-4">
        <p className="text-red-200 text-sm">{error}</p>
      </div>
    )
  }

  const defaultKPIs = {
    'Total Revenue': { value: 125000, trend: 12.5, icon: '💰', status: 'success' as const },
    'Profit': { value: 35000, trend: 8.3, icon: '📈', status: 'success' as const },
    'Orders': { value: 1250, trend: 5.2, icon: '📦', status: 'success' as const },
    'Customer Growth': { value: '23%', trend: 15, icon: '👥', status: 'success' as const },
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 animate-fade-in">
      {Object.entries(defaultKPIs).map(([title, data]) => (
        <KPICard
          key={title}
          title={title}
          value={data.value}
          trend={data.trend}
          icon={data.icon}
          status={data.status}
          sparkline={[10, 15, 8, 20, 12, 25, 18]}
        />
      ))}
    </div>
  )
}
