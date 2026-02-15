import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Типы
export interface RegisterData {
  email: string
  password: string
  name?: string
}

export interface LoginData {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface User {
  id: string
  email: string
  name: string | null
  email_verified: boolean
  is_active: boolean
  created_at: string
}

// Auth API
export const authAPI = {
  async register(data: RegisterData): Promise<TokenResponse> {
    const response = await api.post('/api/v1/auth/register', data)
    return response.data
  },

  async login(data: LoginData): Promise<TokenResponse> {
    const response = await api.post('/api/v1/auth/login', data)
    return response.data
  },

  async refresh(refreshToken: string): Promise<{ access_token: string }> {
    const response = await api.post('/api/v1/auth/refresh', {
      refresh_token: refreshToken,
    })
    return response.data
  },
}

// Users API
export const usersAPI = {
  async getMe(token: string): Promise<User> {
    const response = await api.get('/api/v1/users/me', {
      headers: { Authorization: `Bearer ${token}` },
    })
    return response.data
  },

  async getSubscription(token: string) {
    const response = await api.get('/api/v1/users/me/subscription', {
      headers: { Authorization: `Bearer ${token}` },
    })
    return response.data
  },
}

// Payments API
export const paymentsAPI = {
  async createPayment(token: string, tier: string, period: string) {
    const response = await api.post(
      '/api/v1/payments/create',
      { tier, period },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    return response.data
  },
}

// Helper для сохранения токенов
export const saveTokens = (accessToken: string, refreshToken: string) => {
  localStorage.setItem('access_token', accessToken)
  localStorage.setItem('refresh_token', refreshToken)
}

export const getAccessToken = () => {
  return localStorage.getItem('access_token')
}

export const clearTokens = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

