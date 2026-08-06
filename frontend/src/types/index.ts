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

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  data?: ChatResponse
}
