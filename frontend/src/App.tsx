import { useState, useEffect } from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import ChatPanel from './components/ChatPanel'
import Dashboard from './components/Dashboard'
import SalesPage from './pages/SalesPage'
import FinancePage from './pages/FinancePage'
import MarketingPage from './pages/MarketingPage'
import InventoryPage from './pages/InventoryPage'
import ForecastsPage from './pages/ForecastsPage'
import RecommendationsPage from './pages/RecommendationsPage'
import ReportsPage from './pages/ReportsPage'
import SettingsPage from './pages/SettingsPage'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [darkMode, setDarkMode] = useState(true)

  useEffect(() => {
    // Ensure dark mode is always on
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  const renderContent = () => {
    switch (activeTab) {
      case 'chat':
        return <ChatPanel />
      case 'sales':
        return <SalesPage />
      case 'finance':
        return <FinancePage />
      case 'marketing':
        return <MarketingPage />
      case 'inventory':
        return <InventoryPage />
      case 'forecasts':
        return <ForecastsPage />
      case 'recommendations':
        return <RecommendationsPage />
      case 'reports':
        return <ReportsPage />
      case 'settings':
        return <SettingsPage />
      case 'dashboard':
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="dark bg-slate-900 text-slate-100 min-h-screen">
      <Header darkMode={darkMode} onThemeChange={setDarkMode} />

      <div className="flex">
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />

        <main className="flex-1 overflow-auto h-[calc(100vh-64px)]">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {renderContent()}
          </div>
        </main>
      </div>
    </div>
  )
}

export default App
