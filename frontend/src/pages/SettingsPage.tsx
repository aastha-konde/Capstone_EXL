import { useState } from 'react'

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    theme: 'dark',
    dataRefresh: 'realtime',
    notifications: true,
    apiKey: '••••••••',
  })

  const handleChange = (key: string, value: string | boolean) => {
    setSettings({ ...settings, [key]: value })
  }

  return (
    <div className="space-y-6 max-w-2xl">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-100">Settings</h1>
        <p className="text-slate-400 mt-2">Configure your DecisionLens AI preferences</p>
      </div>

      {/* General Settings */}
      <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-slate-100 mb-6">General</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Theme</label>
            <select
              value={settings.theme}
              onChange={(e) => handleChange('theme', e.target.value)}
              className="w-full bg-slate-700/50 border border-slate-600 rounded px-3 py-2 text-slate-100"
            >
              <option value="dark">Dark Mode</option>
              <option value="light">Light Mode</option>
              <option value="auto">Auto (System)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Data Refresh</label>
            <select
              value={settings.dataRefresh}
              onChange={(e) => handleChange('dataRefresh', e.target.value)}
              className="w-full bg-slate-700/50 border border-slate-600 rounded px-3 py-2 text-slate-100"
            >
              <option value="realtime">Real-time</option>
              <option value="1hour">Every 1 Hour</option>
              <option value="4hour">Every 4 Hours</option>
              <option value="daily">Daily</option>
              <option value="manual">Manual</option>
            </select>
          </div>

          <div className="flex items-center justify-between pt-4">
            <label htmlFor="notifications" className="text-sm font-medium text-slate-300">
              Notifications
            </label>
            <input
              id="notifications"
              type="checkbox"
              checked={settings.notifications}
              onChange={(e) => handleChange('notifications', e.target.checked)}
              className="w-5 h-5 rounded"
            />
          </div>
        </div>
      </div>

      {/* API Configuration */}
      <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-slate-100 mb-6">API Configuration</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Gemini API Key</label>
            <div className="flex gap-2">
              <input
                type="password"
                value={settings.apiKey}
                readOnly
                className="flex-1 bg-slate-700/50 border border-slate-600 rounded px-3 py-2 text-slate-100"
              />
              <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white font-medium text-sm">
                Change
              </button>
            </div>
            <p className="text-xs text-slate-500 mt-2">
              Required for AI Chat and advanced analysis features
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Backend API URL</label>
            <input
              type="text"
              defaultValue="http://localhost:8000"
              className="w-full bg-slate-700/50 border border-slate-600 rounded px-3 py-2 text-slate-100"
            />
          </div>
        </div>
      </div>

      {/* Data & Privacy */}
      <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-slate-100 mb-6">Data & Privacy</h2>
        <div className="space-y-3">
          <button className="w-full text-left px-4 py-3 bg-slate-700/30 hover:bg-slate-700/50 rounded transition">
            <p className="text-slate-100 font-medium">Download Your Data</p>
            <p className="text-xs text-slate-500">Export all your settings and chat history</p>
          </button>

          <button className="w-full text-left px-4 py-3 bg-slate-700/30 hover:bg-slate-700/50 rounded transition">
            <p className="text-slate-100 font-medium">Clear Cache</p>
            <p className="text-xs text-slate-500">Remove cached data to free up space</p>
          </button>

          <button className="w-full text-left px-4 py-3 bg-red-500/10 hover:bg-red-500/20 rounded transition border border-red-500/30">
            <p className="text-red-400 font-medium">Delete Account</p>
            <p className="text-xs text-red-400/70">Permanently delete your account and all data</p>
          </button>
        </div>
      </div>

      {/* About */}
      <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-slate-100 mb-4">About</h2>
        <div className="space-y-2 text-sm text-slate-400">
          <p>
            <span className="text-slate-300 font-medium">Version:</span> 1.0.0
          </p>
          <p>
            <span className="text-slate-300 font-medium">Build:</span> Production
          </p>
          <p>
            <span className="text-slate-300 font-medium">Status:</span>{' '}
            <span className="text-green-400">✓ All Systems Operational</span>
          </p>
          <p className="pt-2">
            DecisionLens AI - Enterprise Decision Intelligence Platform powered by LangGraph and machine learning
            models.
          </p>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end gap-3">
        <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded text-slate-100 font-medium">
          Cancel
        </button>
        <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white font-medium">Save Changes</button>
      </div>
    </div>
  )
}
