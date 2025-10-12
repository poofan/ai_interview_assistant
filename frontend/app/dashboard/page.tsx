'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { usersAPI, getAccessToken, clearTokens } from '@/lib/api'
import { Download, LogOut, CrownIcon } from 'lucide-react'

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [subscription, setSubscription] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadUserData()
  }, [])

  const loadUserData = async () => {
    const token = getAccessToken()
    
    if (!token) {
      router.push('/login')
      return
    }

    try {
      const [userData, subData] = await Promise.all([
        usersAPI.getMe(token),
        usersAPI.getSubscription(token)
      ])
      
      setUser(userData)
      setSubscription(subData)
      setLoading(false)
    } catch (error) {
      console.error('Error loading user data:', error)
      router.push('/login')
    }
  }

  const handleLogout = () => {
    clearTokens()
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
        <div className="text-white">Загрузка...</div>
      </div>
    )
  }

  const tierColors = {
    free: 'text-gray-400',
    pro: 'text-blue-500',
    enterprise: 'text-purple-500'
  }

  const tierNames = {
    free: 'FREE',
    pro: 'PRO',
    enterprise: 'ENTERPRISE'
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900">
      {/* Header */}
      <nav className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
              Hintsage
            </Link>
            <button onClick={handleLogout} className="flex items-center gap-2 text-gray-400 hover:text-white transition">
              <LogOut className="w-4 h-4" />
              Выход
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-white mb-8">Личный кабинет</h1>

        <div className="grid md:grid-cols-3 gap-6">
          {/* User Info */}
          <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Профиль</h2>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-400">Имя</p>
                <p className="text-white">{user?.name || 'Не указано'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Email</p>
                <p className="text-white">{user?.email}</p>
              </div>
            </div>
          </div>

          {/* Subscription */}
          <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-6">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <CrownIcon className="w-5 h-5" />
              Подписка
            </h2>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-400">Тариф</p>
                <p className={`text-2xl font-bold ${tierColors[subscription?.tier as keyof typeof tierColors]}`}>
                  {tierNames[subscription?.tier as keyof typeof tierNames]}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Статус</p>
                <p className="text-green-500">{subscription?.status === 'active' ? 'Активна' : subscription?.status}</p>
              </div>
              {subscription?.tier === 'free' && (
                <Link href="/#pricing" className="block mt-4 text-center bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg transition">
                  Upgrade до PRO
                </Link>
              )}
            </div>
          </div>

          {/* Download */}
          <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-6">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Download className="w-5 h-5" />
              Приложение
            </h2>
            <div className="space-y-3">
              <p className="text-gray-400 text-sm">
                Скачайте desktop приложение для доступа к AI ассистенту
              </p>
              <a
                href="https://smartsobes.ru/download/Hintsage.exe"
                className="block text-center bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg transition"
              >
                Скачать .exe
              </a>
              <p className="text-xs text-gray-500 text-center">
                Версия 1.0.0 • Windows
              </p>
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="mt-8 bg-gray-800/50 border border-gray-700 rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-4">Доступные функции</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {subscription?.features?.map((feature: string) => (
              <div key={feature} className="flex items-center gap-2 text-gray-300">
                <span className="text-green-500">✓</span>
                <span>{formatFeature(feature)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

function formatFeature(feature: string): string {
  const featureNames: Record<string, string> = {
    basic_stt: 'Базовое распознавание речи (Vosk)',
    advanced_stt: 'Продвинутое распознавание (Whisper GPU)',
    limited_requests: 'Ограниченные запросы (5/час)',
    unlimited_requests: 'Безлимитные запросы',
    standard_context: 'Стандартный контекст (10 сообщений)',
    extended_context: 'Расширенный контекст (30 сообщений)',
    custom_prompts: 'Кастомные промпты',
    screenshot_ocr: 'OCR скриншотов',
    priority_support: 'Приоритетная поддержка',
    team_sharing: 'Командный доступ',
    custom_integrations: 'Кастомные интеграции',
    dedicated_support: 'Выделенная поддержка'
  }
  
  return featureNames[feature] || feature
}

