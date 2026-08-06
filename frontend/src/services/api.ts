import axios, { AxiosInstance } from 'axios'

// Determine API base URL: use env var, or derive from current location for Dev Tunnels
const getAPIBaseURL = (): string => {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }

  // For Dev Tunnels: if frontend is on https://r3r5029m-3000.inc1.devtunnels.ms
  // derive backend from the hostname pattern (r3r5029m is the tunnel ID)
  if (typeof window !== 'undefined' && window.location.hostname.includes('.devtunnels.')) {
    const parts = window.location.hostname.split('-')
    if (parts.length > 0) {
      const tunnelId = parts[0]
      return `https://${tunnelId}-8000.inc1.devtunnels.ms`
    }
  }

  return 'http://localhost:8000'
}

const API_BASE_URL = getAPIBaseURL()

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutes for agent pipeline
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Types
export interface ChatRequest {
  question: string
  session_id?: string
}

export interface KPI {
  [key: string]: number | string
}

export interface Trend {
  metric: string
  direction: 'up' | 'down' | 'stable'
  percentage: number
  period: string
}

export interface Anomaly {
  metric: string
  value: number
  expected: number
  severity: 'low' | 'medium' | 'high'
  description: string
}

export interface Forecast {
  metric: string
  value: number
  confidence_interval: {
    lower: number
    upper: number
  }
  period: string
  model: string
}

export interface Recommendation {
  id: string
  title: string
  description: string
  priority: 'high' | 'medium' | 'low'
  expected_impact: string
  department?: string
  estimated_cost?: number
  estimated_savings?: number
}

export interface Analytics {
  kpis?: KPI
  trends?: Trend[]
  anomalies?: Anomaly[]
  root_causes?: string[]
}

export interface ExecutiveSummary {
  narrative: string
  key_findings: string[]
  risks: string[]
  next_steps: string[]
}

export interface ChatResponse {
  session_id: string
  question: string
  intent: string
  sql_result?: any
  analytics?: Analytics
  forecasts?: Forecast[]
  recommendations?: Recommendation[]
  executive_summary?: ExecutiveSummary
  response_time_ms: number
}

export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy'
  version: string
  environment: string
  timestamp: string
  database: string
  duckdb: string
}

export interface StatusResponse {
  app: string
  version: string
  environment: string
  database: string
  duckdb: string
  timestamp: string
  features: {
    rag: boolean
    forecasting: boolean
    anomaly_detection: boolean
    power_bi_embed: boolean
  }
}

// API Methods
export const api = {
  // Health & Status
  getHealth: async (): Promise<HealthResponse> => {
    const { data } = await apiClient.get('/health')
    return data
  },

  getStatus: async (): Promise<StatusResponse> => {
    const { data } = await apiClient.get('/status')
    return data
  },

  // Chat & Analysis
  chat: async (request: ChatRequest): Promise<ChatResponse> => {
    const { data } = await apiClient.post('/api/chat', request)
    return data
  },

  // KPIs
  getKPIs: async (filters?: Record<string, any>): Promise<any> => {
    const { data } = await apiClient.get('/api/kpis', { params: filters })
    return data
  },

  // Forecasts
  getForecasts: async (metric?: string, filters?: Record<string, any>): Promise<Forecast[]> => {
    const params = { ...filters }
    if (metric) params.metric = metric
    const { data } = await apiClient.get('/api/forecasts', { params })
    return data
  },

  // Anomalies
  getAnomalies: async (filters?: Record<string, any>): Promise<Anomaly[]> => {
    const { data } = await apiClient.get('/api/anomalies', { params: filters })
    return data
  },

  // Recommendations
  getRecommendations: async (filters?: Record<string, any>): Promise<Recommendation[]> => {
    const { data } = await apiClient.get('/api/recommendations', { params: filters })
    return data
  },

  // Reports
  generateReport: async (format: 'pdf' | 'pptx', filters?: Record<string, any>): Promise<Blob> => {
    const { data } = await apiClient.post(
      `/api/reports/${format}`,
      filters,
      { responseType: 'blob' }
    )
    return data
  },

  // Analytics
  getAnalytics: async (question?: string, filters?: Record<string, any>): Promise<Analytics> => {
    const params = { ...filters }
    if (question) params.question = question
    const { data } = await apiClient.get('/api/analytics', { params })
    return data
  },
}

export default apiClient
