import axios, { AxiosInstance, AxiosError } from 'axios'
import {
  ChatResponse,
  HealthResponse,
  StatusResponse,
  KPI,
  Trend,
  Anomaly,
  Forecast,
  Recommendation,
  Analytics,
} from '../types'

// Re-export types for backward compatibility
export type { ChatResponse, HealthResponse, StatusResponse, KPI, Trend, Anomaly, Forecast, Recommendation, Analytics }

// Detect environment and determine API base URL
const getAPIBaseURL = (): string => {
  // 1. Check for explicit environment variable (highest priority)
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }

  // 2. For Dev Tunnels: detect tunnel ID from hostname and derive backend URL
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname

    // Dev Tunnels pattern: r3r5029m-3000.inc1.devtunnels.ms → r3r5029m-8000.inc1.devtunnels.ms
    if (hostname.includes('.devtunnels.')) {
      const parts = hostname.split('-')
      if (parts.length > 0) {
        const tunnelId = parts[0]
        const backendURL = `https://${tunnelId}-8000.inc1.devtunnels.ms`
        console.log(`[API] Detected Dev Tunnel. Using backend: ${backendURL}`)
        return backendURL
      }
    }

    // 3. Docker networking: if hostname is not localhost, assume Docker internal networking
    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
      // For Docker Compose, backend service is at http://backend:8000
      const backendURL = `http://${hostname}:8000`
      console.log(`[API] Detected Docker environment. Using backend: ${backendURL}`)
      return backendURL
    }
  }

  // 4. Default to localhost for local development
  return 'http://localhost:8000'
}

const API_BASE_URL = getAPIBaseURL()

// Create axios instance with optimal configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutes for agent pipeline
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

// Add request interceptor for authentication and logging
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  if (import.meta.env.DEV) {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
  }

  return config
})

// Add response interceptor for error handling and logging
apiClient.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log(`[API] ✓ ${response.status} ${response.config.url}`)
    }
    return response
  },
  (error: AxiosError) => {
    if (import.meta.env.DEV) {
      console.error(`[API] ✗ ${error.config?.url}`, error.response?.status, error.message)
    }

    // Enhance error messages
    if (!error.response) {
      // Network error
      return Promise.reject(new Error(
        'Network error. Unable to reach backend. Check your connection and CORS configuration.'
      ))
    }

    return Promise.reject(error)
  }
)

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
  chat: async (request: { question: string; session_id?: string }): Promise<ChatResponse> => {
    const { data } = await apiClient.post('/api/chat', request)
    return data
  },

  // KPIs
  getKPIs: async (filters?: Record<string, any>): Promise<any> => {
    const { data } = await apiClient.get('/api/kpis', { params: filters })
    return data
  },

  // Forecasts
  getForecasts: async (metric?: string, filters?: Record<string, any>): Promise<any[]> => {
    const params = { ...filters }
    if (metric) params.metric = metric
    const { data } = await apiClient.get('/api/forecasts', { params })
    return data
  },

  // Anomalies
  getAnomalies: async (filters?: Record<string, any>): Promise<any[]> => {
    const { data } = await apiClient.get('/api/anomalies', { params: filters })
    return data
  },

  // Recommendations
  getRecommendations: async (filters?: Record<string, any>): Promise<any[]> => {
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
  getAnalytics: async (question?: string, filters?: Record<string, any>): Promise<any> => {
    const params = { ...filters }
    if (question) params.question = question
    const { data } = await apiClient.get('/api/analytics', { params })
    return data
  },
}

export default apiClient
export { API_BASE_URL }
