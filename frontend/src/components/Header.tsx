import { useState, useEffect } from 'react'
import { api } from '../services/api'

interface HeaderProps {
  darkMode: boolean
  onThemeChange: (dark: boolean) => void
}

export default function Header({ darkMode, onThemeChange }: HeaderProps) {
  const [time, setTime] = useState(new Date())
  const [connectionStatus, setConnectionStatus] = useState<'online' | 'offline' | 'checking'>('checking')

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    const checkConnection = async () => {
      try {
        await api.getHealth()
        setConnectionStatus('online')
      } catch {
        setConnectionStatus('offline')
      }
    }

    checkConnection()
    const interval = setInterval(checkConnection, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <header className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border-b border-slate-700/50 sticky top-0 z-50 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          {/* Logo & Title */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">DL</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">DecisionLens AI</h1>
              <p className="text-xs text-slate-400">Enterprise Decision Intelligence</p>
            </div>
          </div>

          {/* Center - Time & Status */}
          <div className="hidden md:flex items-center gap-6">
            <div className="text-center">
              <p className="text-slate-400 text-xs">Current Time</p>
              <p className="text-white font-mono text-sm">{time.toLocaleTimeString()}</p>
            </div>
            <div className="h-8 w-px bg-slate-700/50" />
            <div className="text-center">
              <p className="text-slate-400 text-xs">Backend Status</p>
              <div className="flex items-center gap-2 justify-center mt-1">
                <span className={`w-2 h-2 rounded-full ${
                  connectionStatus === 'online' ? 'bg-emerald-500 animate-pulse' :
                  connectionStatus === 'checking' ? 'bg-amber-500 animate-pulse' :
                  'bg-red-500'
                }`} />
                <p className="text-white font-mono text-sm capitalize">{connectionStatus}</p>
              </div>
            </div>
          </div>

          {/* Right - Controls */}
          <div className="flex items-center gap-4">
            <button
              onClick={() => onThemeChange(!darkMode)}
              className="p-2 rounded-lg hover:bg-slate-700/50 transition"
              title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {darkMode ? '☀️' : '🌙'}
            </button>
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center cursor-pointer hover:shadow-lg transition">
              <span className="text-white font-bold">👤</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
