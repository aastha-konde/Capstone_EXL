export default function ReportsPage() {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-100">Reports</h1>
        <p className="text-slate-400 mt-2">Generate and manage business reports</p>
      </div>

      {/* Coming Soon */}
      <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-12 text-center">
        <div className="text-6xl mb-4">📄</div>
        <h2 className="text-2xl font-bold text-slate-100 mb-2">Reports Feature</h2>
        <p className="text-slate-400 mb-6 max-w-md mx-auto">
          This feature will allow you to generate, schedule, and export custom business reports with all the data
          from your analytics pages.
        </p>
        <div className="inline-block bg-blue-500/20 border border-blue-500/50 rounded-lg p-6">
          <p className="text-blue-400 text-sm">Coming in v1.1</p>
        </div>
      </div>

      {/* Feature Preview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-4xl mb-3">📊</div>
          <h3 className="font-semibold text-slate-100 mb-2">Custom Reports</h3>
          <p className="text-slate-400 text-sm">Create reports with selected metrics and visualizations</p>
        </div>
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-4xl mb-3">📅</div>
          <h3 className="font-semibold text-slate-100 mb-2">Scheduled Reports</h3>
          <p className="text-slate-400 text-sm">Automatically generate and email reports on a schedule</p>
        </div>
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
          <div className="text-4xl mb-3">📥</div>
          <h3 className="font-semibold text-slate-100 mb-2">Export Formats</h3>
          <p className="text-slate-400 text-sm">Download reports in PDF, Excel, PowerPoint formats</p>
        </div>
      </div>
    </div>
  )
}
