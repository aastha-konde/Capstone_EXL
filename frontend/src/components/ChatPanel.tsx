import { useState } from 'react'
import axios from 'axios'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export default function ChatPanel() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

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
      const response = await axios.post(
        'http://localhost:8000/api/chat',
        { question },
        { timeout: 60000 }
      )

      const data = response.data

      // Build assistant response
      let responseText = `**Analysis Complete**\n\n`

      if (data.intent) {
        responseText += `**Intent:** ${data.intent}\n\n`
      }

      if (data.analytics) {
        responseText += `**KPIs:**\n`
        const kpis = data.analytics.kpis || {}
        for (const [key, val] of Object.entries(kpis).slice(0, 5)) {
          responseText += `• ${key}: ${JSON.stringify(val)}\n`
        }
        responseText += '\n'
      }

      if (data.recommendations && data.recommendations.length > 0) {
        responseText += `**Recommendations:**\n`
        data.recommendations.slice(0, 3).forEach((rec: any, i: number) => {
          responseText += `${i+1}. ${rec.title} [${rec.priority}]\n`
          responseText += `   Impact: ${rec.expected_impact}\n`
        })
        responseText += '\n'
      }

      if (data.executive_summary) {
        responseText += `**Summary:** ${data.executive_summary.narrative}\n`
      }

      responseText += `\n*Response time: ${data.response_time_ms?.toFixed(2) || '?'}ms*`

      const assistantMessage: Message = {
        role: 'assistant',
        content: responseText,
        timestamp: new Date().toLocaleTimeString(),
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
                <div className="bg-gray-200 dark:bg-gray-700 px-4 py-2 rounded-lg">
                  <p className="text-sm text-gray-700 dark:text-gray-300">🤔 Analyzing...</p>
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
