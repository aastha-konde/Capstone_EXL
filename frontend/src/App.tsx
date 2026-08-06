import { useState, useEffect } from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import ChatPanel from './components/ChatPanel'
import Dashboard from './components/Dashboard'

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
