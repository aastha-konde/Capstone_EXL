import { useState } from 'react'
import { api, ChatResponse } from '../services/api'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  data?: ChatResponse
}

export default function ChatPanel() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [sessionId, setSessionId] = useState<string | undefined>()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!question.trim()) return

    // Add user message
    const userMessage: Message = {
      role: 'user',
      content: question,
      timestamp: new Date().toLocaleTimeString(),
    }
    setMessages(prev => [...prev, userMessage])
    setQuestion('')
    setLoading(true)
    setError('')

    try {
      const response = await api.chat({
        question,
        session_id: sessionId,
      })

      if (!sessionId) {
        setSessionId(response.session_id)
      }

      // Build assistant response
      let responseText = `**Analysis Complete** (${response.response_time_ms.toFixed(0)}ms)\n\n`

      if (response.intent) {
        responseText += `**Intent:** ${response.intent}\n\n`
      }

      if (response.analytics?.kpis) {
        responseText += `**Key Metrics:**\n`
        const kpis = response.analytics.kpis
        const kpiEntries = Object.entries(kpis).slice(0, 5)
        for (const [key, val] of kpiEntries) {
          const formatted = typeof val === 'number'
            ? val.toLocaleString(undefined, { maximumFractionDigits: 2 })
            : val
          responseText += `• **${key.replace(/_/g, ' ')}:** ${formatted}\n`
        }
        responseText += '\n'
      }

      if (response.analytics?.trends && response.analytics.trends.length > 0) {
        responseText += `**Trends:**\n`
        response.analytics.trends.slice(0, 3).forEach((trend) => {
          const icon = trend.direction === 'up' ? '📈' : trend.direction === 'down' ? '📉' : '➡️'
          responseText += `• ${trend.metric}: ${icon} ${trend.percentage > 0 ? '+' : ''}${trend.percentage.toFixed(1)}% (${trend.period})\n`
        })
        responseText += '\n'
      }

      if (response.forecasts && response.forecasts.length > 0) {
        responseText += `**Forecasts:**\n`
        response.forecasts.slice(0, 2).forEach((f) => {
          responseText += `• ${f.metric}: ${f.value.toLocaleString(undefined, { maximumFractionDigits: 1 })} (${f.period})\n`
        })
        responseText += '\n'
      }

      if (response.recommendations && response.recommendations.length > 0) {
        responseText += `**Top Recommendations:**\n`
        response.recommendations.slice(0, 3).forEach((rec, i) => {
          const priorityEmoji = rec.priority === 'high' ? '🔴' : rec.priority === 'medium' ? '🟡' : '🟢'
          responseText += `${i+1}. ${priorityEmoji} **${rec.title}** [${rec.priority.toUpperCase()}]\n`
          responseText += `   Impact: ${rec.expected_impact}\n`
        })
        responseText += '\n'
      }

      if (response.executive_summary) {
        responseText += `**Executive Summary:**\n`
        responseText += `${response.executive_summary.narrative}\n`
      }

      const assistantMessage: Message = {
        role: 'assistant',
        content: responseText,
        timestamp: new Date().toLocaleTimeString(),
        data: response,
      }
      setMessages(prev => [...prev, assistantMessage])

    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to get response'
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Chat Panel */}
      <div className="lg:col-span-2">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden flex flex-col h-screen max-h-screen md:max-h-96 lg:max-h-96">
          {/* Chat History */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 dark:text-gray-400 py-8">
                <p className="text-lg font-semibold">💬 Ask a business question</p>
                <p className="text-sm mt-2">Examples:</p>
                <ul className="mt-3 text-xs space-y-1">
                  <li>"Why did revenue decline last quarter?"</li>
                  <li>"Which region is underperforming?"</li>
                  <li>"What should we do to improve profitability?"</li>
                </ul>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs px-4 py-2 rounded-lg ${
                      msg.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100'
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                    <p className="text-xs mt-1 opacity-70">{msg.timestamp}</p>
                  </div>
                </div>
              ))
            )}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-200 dark:bg-gray-700 px-4 py-3 rounded-lg max-w-sm">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">🤔</span>
                    <div>
                      <p className="text-sm text-gray-700 dark:text-gray-300 font-semibold">Analyzing your question...</p>
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">This may take up to 2 minutes (Running agent pipeline)</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <form onSubmit={handleSubmit} className="border-t border-gray-200 dark:border-gray-700 p-4">
            {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
            <div className="flex space-x-2">
              <input
                type="text"
                value={question}
                onChange={e => setQuestion(e.target.value)}
                placeholder="Ask a question..."
                disabled={loading}
                className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              />
              <button
                type="submit"
                disabled={loading || !question.trim()}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition"
              >
                Send
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Info Panel */}
      <div className="space-y-4">
        <div className="bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg p-4">
          <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">💡 Tips</h3>
          <ul className="text-sm text-blue-800 dark:text-blue-200 space-y-1">
            <li>• Ask "why" to understand root causes</li>
            <li>• Ask "what" to get predictions</li>
            <li>• Ask "how" to get recommendations</li>
            <li>• Add regions/products for specificity</li>
          </ul>
        </div>

        <div className="bg-green-50 dark:bg-green-900 border border-green-200 dark:border-green-700 rounded-lg p-4">
          <h3 className="font-semibold text-green-900 dark:text-green-100 mb-2">✅ Features</h3>
          <ul className="text-sm text-green-800 dark:text-green-200 space-y-1">
            <li>✓ SQL analysis</li>
            <li>✓ KPI calculation</li>
            <li>✓ Trend detection</li>
            <li>✓ Forecasting</li>
            <li>✓ Recommendations</li>
            <li>✓ Executive summaries</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
