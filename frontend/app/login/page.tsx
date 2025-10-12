'use client'

import { useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { authAPI, saveTokens } from '@/lib/api'

export default function LoginPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const callback = searchParams.get('callback')
  
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      // Логин через API
      const response = await authAPI.login({ email, password })
      
      // Сохраняем токены
      saveTokens(response.access_token, response.refresh_token)
      
      // Если есть callback (от Desktop App) - редиректим с токеном
      if (callback) {
        window.location.href = `${callback}?token=${response.access_token}`
      } else {
        // Иначе редиректим на dashboard
        router.push('/dashboard')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка входа. Проверьте email и пароль.')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link href="/" className="text-3xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
            Hintsage
          </Link>
          <p className="text-gray-400 mt-2">Вход в систему</p>
        </div>

        {/* Form */}
        <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Error */}
            {error && (
              <div className="bg-red-500/10 border border-red-500 text-red-500 p-4 rounded-lg">
                {error}
              </div>
            )}

            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500 transition"
                placeholder="your@email.com"
              />
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                Пароль
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500 transition"
                placeholder="••••••••"
              />
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white py-3 rounded-lg font-semibold transition"
            >
              {loading ? 'Вход...' : 'Войти'}
            </button>
          </form>

          {/* Links */}
          <div className="mt-6 text-center">
            <p className="text-gray-400">
              Нет аккаунта?{' '}
              <Link href="/register" className="text-blue-500 hover:text-blue-400">
                Зарегистрироваться
              </Link>
            </p>
          </div>

          {/* Test Credentials */}
          {callback && (
            <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500 rounded-lg">
              <p className="text-sm text-blue-400 font-semibold mb-2">Тестовые аккаунты:</p>
              <ul className="text-xs text-gray-400 space-y-1">
                <li>FREE: free@test.com / password123</li>
                <li>PRO: pro@test.com / password123</li>
                <li>ENTERPRISE: enterprise@test.com / password123</li>
              </ul>
            </div>
          )}
        </div>

        {/* Back */}
        <div className="text-center mt-6">
          <Link href="/" className="text-gray-400 hover:text-white transition">
            ← Вернуться на главную
          </Link>
        </div>
      </div>
    </div>
  )
}

