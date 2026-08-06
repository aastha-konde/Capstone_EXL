interface NavItem {
  id: string
  label: string
  icon: string
  badge?: number
}

interface SidebarProps {
  activeTab: string
  onTabChange: (tab: string) => void
}

const navItems: NavItem[] = [
  { id: 'dashboard', label: 'Dashboard', icon: '📊' },
  { id: 'chat', label: 'AI Chat', icon: '💬' },
  { id: 'sales', label: 'Sales', icon: '💰' },
  { id: 'finance', label: 'Finance', icon: '📈' },
  { id: 'marketing', label: 'Marketing', icon: '📢' },
  { id: 'inventory', label: 'Inventory', icon: '📦' },
  { id: 'forecasts', label: 'Forecasts', icon: '🔮' },
  { id: 'recommendations', label: 'Recommendations', icon: '💡' },
  { id: 'reports', label: 'Reports', icon: '📄' },
  { id: 'settings', label: 'Settings', icon: '⚙️' },
]

export default function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  return (
    <aside className="w-64 bg-slate-800/50 border-r border-slate-700/50 backdrop-blur-xl h-screen overflow-y-auto sticky top-16">
      <nav className="p-4 space-y-2">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onTabChange(item.id)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition ${
              activeTab === item.id
                ? 'bg-blue-600/20 text-blue-400 border border-blue-500/50'
                : 'text-slate-300 hover:bg-slate-700/50 border border-transparent'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span className="flex-1 text-left font-medium text-sm">{item.label}</span>
            {item.badge && (
              <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full">
                {item.badge}
              </span>
            )}
          </button>
        ))}
      </nav>

      {/* Sidebar Footer */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-slate-700/50">
        <div className="bg-slate-700/30 rounded-lg p-4 text-center">
          <p className="text-xs text-slate-400 mb-2">v1.0.0</p>
          <p className="text-xs text-slate-500">Powered by LangGraph</p>
        </div>
      </div>
    </aside>
  )
}
