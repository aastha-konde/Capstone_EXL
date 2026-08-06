import { useState, useRef, useEffect } from 'react'
import { api } from '../services/api'
import { TypingIndicator, LoadingSpinner } from './Skeleton'
import { Message } from '../types'

const SUGGESTED_PROMPTS = [
  "What are the top 3 revenue drivers?",
  "Show me sales trends for the last quarter",
  "What are the main profit risks?",
  "Forecast next month's revenue",
  "Which products have the best margins?",
]

export default function ChatPanel() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [sessionId, setSessionId] = useState<string | undefined>()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSuggestedPrompt = (prompt: string) => {
    setQuestion(prompt)
    inputRef.current?.focus()
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!question.trim()) return

    const userMessage: Message = {
      role: 'user',
      content: question,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
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

      // Build comprehensive response
      let responseText = `**Analysis Complete** ✓\n\n`

      if (response.intent) {
        responseText += `**Intent:** ${response.intent}\n\n`
      }

      if (response.analytics?.kpis) {
        responseText += `**📊 Key Metrics**\n`
        const kpiEntries = Object.entries(response.analytics.kpis).slice(0, 6)
        kpiEntries.forEach(([key, val]) => {
          const formatted = typeof val === 'number'
            ? val.toLocaleString(undefined, { maximumFractionDigits: 2 })
            : val
          responseText += `• **${key.replace(/_/g, ' ')}:** ${formatted}\n`
        })
        responseText += '\n'
      }

      if (response.analytics?.trends && response.analytics.trends.length > 0) {
        responseText += `**📈 Trends**\n`
        response.analytics.trends.slice(0, 3).forEach((trend) => {
          const icon = trend.direction === 'up' ? '📉' : trend.direction === 'down' ? '📉' : '➡️'
          responseText += `• ${trend.metric}: ${icon} ${trend.percentage > 0 ? '+' : ''}${trend.percentage.toFixed(1)}% (${trend.period})\n`
        })
        responseText += '\n'
      }

      if (response.analytics?.anomalies && response.analytics.anomalies.length > 0) {
        responseText += `**⚠️ Anomalies Detected**\n`
        response.analytics.anomalies.slice(0, 3).forEach((anom) => {
          const severityEmoji = anom.severity === 'high' ? '🔴' : anom.severity === 'medium' ? '🟡' : '🟢'
          responseText += `${severityEmoji} ${anom.metric}: ${anom.description}\n`
        })
        responseText += '\n'
      }

      if (response.forecasts && response.forecasts.length > 0) {
        responseText += `**🔮 Forecasts**\n`
        response.forecasts.slice(0, 3).forEach((f) => {
          const value = f.value.toLocaleString(undefined, { maximumFractionDigits: 1 })
          const lower = f.confidence_interval.lower.toLocaleString(undefined, { maximumFractionDigits: 0 })
          const upper = f.confidence_interval.upper.toLocaleString(undefined, { maximumFractionDigits: 0 })
          responseText += `• ${f.metric}: ${value} (95% CI: ${lower}-${upper})\n`
        })
        responseText += '\n'
      }

      if (response.recommendations && response.recommendations.length > 0) {
        responseText += `**💡 Top Recommendations**\n`
        response.recommendations.slice(0, 3).forEach((rec, i) => {
          const priorityEmoji = rec.priority === 'high' ? '🔴' : rec.priority === 'medium' ? '🟡' : '🟢'
          responseText += `${i+1}. ${priorityEmoji} **${rec.title}**\n`
          responseText += `   Impact: ${rec.expected_impact}\n`
          if (rec.estimated_savings) {
            responseText += `   Potential Savings: $${rec.estimated_savings.toLocaleString()}\n`
          }
        })
        responseText += '\n'
      }

      if (response.executive_summary) {
        responseText += `**📋 Executive Summary**\n`
        responseText += `${response.executive_summary.narrative}\n\n`

        if (response.executive_summary.key_findings.length > 0) {
          responseText += `**Key Findings:**\n`
          response.executive_summary.key_findings.forEach(f => {
            responseText += `• ${f}\n`
          })
          responseText += '\n'
        }

        if (response.executive_summary.risks.length > 0) {
          responseText += `**Risks:**\n`
          response.executive_summary.risks.forEach(r => {
            responseText += `• ${r}\n`
          })
          responseText += '\n'
        }
      }

      responseText += `\n---\n⏱️ Response time: ${response.response_time_ms}ms`

      const assistantMessage: Message = {
        role: 'assistant',
        content: responseText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        data: response,
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (err: any) {
      const errorMsg = err.message || err.response?.data?.detail || 'Failed to process request'
      setError(errorMsg)
      console.error('Chat Error:', err)

      const errorMessage: Message = {
        role: 'assistant',
        content: `❌ **Error**\n\n${errorMsg}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const clearChat = () => {
    setMessages([])
    setSessionId(undefined)
    setError('')
  }

  return (
    <div className="flex flex-col h-[calc(100vh-120px)] gap-4">
      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 pb-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full gap-8">
            <div className="text-center">
              <div className="text-5xl mb-4">💬</div>
              <h2 className="text-2xl font-bold text-white mb-2">AI Business Analyst</h2>
              <p className="text-slate-400">Ask any business question. I'll analyze your data and provide actionable insights.</p>
            </div>

            {/* Suggested Prompts */}
            <div className="w-full max-w-2xl">
              <p className="text-slate-400 text-sm mb-3">Suggested questions:</p>
              <div className="grid grid-cols-1 gap-2">
                {SUGGESTED_PROMPTS.map((prompt, i) => (
                  <button
                    key={i}
                    onClick={() => handleSuggestedPrompt(prompt)}
                    className="text-left px-4 py-3 rounded-lg bg-slate-800/50 hover:bg-slate-700/50 border border-slate-700/50 hover:border-slate-600/50 text-slate-300 hover:text-white transition text-sm"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
            >
              <div
                className={`max-w-2xl rounded-xl px-4 py-3 ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-tr-none'
                    : 'bg-slate-800 text-slate-100 rounded-tl-none border border-slate-700'
                }`}
              >
                {msg.role === 'assistant' && (
                  <div className="text-xs text-slate-400 mb-2">{msg.timestamp}</div>
                )}
                <div className="prose prose-invert max-w-none text-sm space-y-2">
                  {msg.content.split('\n').map((line, j) => {
                    if (line.startsWith('###')) {
                      return <h4 key={j} className="font-bold mt-3 text-white">{line.replace('###', '').trim()}</h4>
                    }
                    if (line.startsWith('##')) {
                      return <h3 key={j} className="font-bold mt-3 text-lg text-white">{line.replace('##', '').trim()}</h3>
                    }
                    if (line.startsWith('**')) {
                      return <p key={j} className="font-semibold">{line}</p>
                    }
                    if (line.startsWith('•')) {
                      return <p key={j} className="ml-4 text-slate-300">{line}</p>
                    }
                    return <p key={j} className="text-slate-300">{line}</p>
                  })}
                </div>
                {msg.role === 'user' && (
                  <div className="text-xs text-blue-100 mt-1 opacity-70">{msg.timestamp}</div>
                )}
              </div>
            </div>
          ))
        )}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-800 text-slate-100 rounded-xl rounded-tl-none px-4 py-3 border border-slate-700">
              <TypingIndicator />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="space-y-3">
        {error && (
          <div className="bg-red-900/20 border border-red-700/50 rounded-lg p-3 text-red-200 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask me anything about your business..."
            disabled={loading}
            className="flex-1 px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition flex items-center gap-2"
          >
            {loading ? <LoadingSpinner /> : '→'}
          </button>
        </form>

        {messages.length > 0 && (
          <button
            onClick={clearChat}
            className="w-full py-2 text-slate-400 hover:text-slate-300 transition text-sm"
          >
            Clear conversation
          </button>
        )}
      </div>
    </div>
  )
}
