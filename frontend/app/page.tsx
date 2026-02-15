import Link from 'next/link'
import { ArrowRight, Zap, Shield, Cpu, Check, Star } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 border-b border-gray-800 bg-black/80 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="text-xl font-semibold text-white">
              Hintsage
            </Link>
            <div className="hidden md:flex items-center space-x-8">
              <Link href="#features" className="text-gray-400 hover:text-white text-sm transition-colors">
                Возможности
              </Link>
              <Link href="#pricing" className="text-gray-400 hover:text-white text-sm transition-colors">
                Тарифы
              </Link>
              <Link href="/login" className="text-gray-400 hover:text-white text-sm transition-colors">
                Войти
              </Link>
              <Link href="/register" className="bg-white text-black px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-100 transition-colors">
                Начать бесплатно
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-gray-900 border border-gray-800 text-sm text-gray-300 mb-8">
            <Star className="w-4 h-4 mr-2 text-yellow-400" />
            Новый AI-ассистент для разработчиков
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            Проходите интервью с{' '}
            <span className="text-gray-400">уверенностью</span>
          </h1>
          
          <p className="text-xl text-gray-400 mb-12 max-w-2xl mx-auto leading-relaxed">
            Hintsage помогает разработчикам уверенно проходить технические интервью с помощью AI-подсказок в реальном времени
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link href="/register" className="bg-white text-black px-8 py-4 rounded-lg font-medium hover:bg-gray-100 transition-colors inline-flex items-center gap-2">
              Начать бесплатно
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link href="#pricing" className="border border-gray-700 text-white px-8 py-4 rounded-lg font-medium hover:border-gray-600 transition-colors">
              Посмотреть тарифы
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Все необходимое для успешного интервью
            </h2>
            <p className="text-gray-400 text-lg">
              Мощные инструменты, которые помогут вам показать свои лучшие навыки
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-8">
              <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-6">
                <Zap className="w-6 h-6 text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold mb-3">GPU Ускорение</h3>
              <p className="text-gray-400 leading-relaxed">
                Whisper STT с поддержкой CUDA для мгновенного распознавания речи
              </p>
            </div>
            
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-8">
              <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center mb-6">
                <Shield className="w-6 h-6 text-green-400" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Конфиденциальность</h3>
              <p className="text-gray-400 leading-relaxed">
                Антидетект защита от скриншотов и захвата экрана
              </p>
            </div>
            
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-8">
              <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-6">
                <Cpu className="w-6 h-6 text-purple-400" />
              </div>
              <h3 className="text-xl font-semibold mb-3">AI Подсказки</h3>
              <p className="text-gray-400 leading-relaxed">
                GPT-4 анализирует вопросы и дает точные ответы в реальном времени
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-20 px-6 bg-gray-900/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Простые и прозрачные тарифы
            </h2>
            <p className="text-gray-400 text-lg">
              Выберите план, который подходит именно вам
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Free */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-8">
              <h3 className="text-xl font-semibold mb-2">Free</h3>
              <div className="mb-6">
                <span className="text-3xl font-bold">0 ₽</span>
                <span className="text-gray-400 ml-2">навсегда</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center gap-3 text-gray-300">
                  <Check className="w-5 h-5 text-gray-500" />
                  Базовый STT (Vosk)
                </li>
                <li className="flex items-center gap-3 text-gray-300">
                  <Check className="w-5 h-5 text-gray-500" />
                  5 запросов в час
                </li>
                <li className="flex items-center gap-3 text-gray-300">
                  <Check className="w-5 h-5 text-gray-500" />
                  Стандартный контекст
                </li>
              </ul>
              <Link href="/register" className="block text-center py-3 border border-gray-700 rounded-lg hover:border-gray-600 transition-colors">
                Начать бесплатно
              </Link>
            </div>
            
            {/* Pro */}
            <div className="bg-gray-900 border-2 border-white rounded-xl p-8 relative">
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <span className="bg-white text-black px-4 py-1 rounded-full text-sm font-medium">
                  Популярный
                </span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Pro</h3>
              <div className="mb-6">
                <span className="text-3xl font-bold">1,499 ₽</span>
                <span className="text-gray-400 ml-2">в месяц</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center gap-3 text-gray-300">
                  <Check className="w-5 h-5 text-white" />
                  Whisper GPU STT
                </li>
                <li className="flex items-center gap-3 text-gray-300">
                  <Check className="w-5 h-5 text-white" />
                  Безлимитные запросы
                </li>
                <li className="flex items-center gap-3 text-gray-300">
                  <Check className="w-5 h-5 text-white" />
                  Расширенный контекст
                </li>
                <li className="flex items-center gap-3 text-gray-300">
                  <Check className="w-5 h-5 text-white" />
                  OCR скриншотов
          </li>
                <li className="flex items-center gap-3 text-gray-300">
                  <Check className="w-5 h-5 text-white" />
                  Приоритетная поддержка
          </li>
              </ul>
              <Link href="/register" className="block text-center py-3 bg-white text-black rounded-lg hover:bg-gray-100 transition-colors">
                Купить Pro
              </Link>
            </div>
            
            {/* Enterprise */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-8">
              <h3 className="text-xl font-semibold mb-2">Enterprise</h3>
              <div className="mb-6">
                <span className="text-3xl font-bold">7,490 ₽</span>
                <span className="text-gray-400 ml-2">в месяц</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center gap-3 text-gray-300">
                  <Check className="w-5 h-5 text-gray-500" />
                  Все из Pro
                </li>
                <li className="flex items-center gap-3 text-gray-300">
                  <Check className="w-5 h-5 text-gray-500" />
                  Командный доступ
                </li>
                <li className="flex items-center gap-3 text-gray-300">
                  <Check className="w-5 h-5 text-gray-500" />
                  Кастомные интеграции
                </li>
                <li className="flex items-center gap-3 text-gray-300">
                  <Check className="w-5 h-5 text-gray-500" />
                  SLA гарантии
                </li>
              </ul>
              <Link href="/register" className="block text-center py-3 border border-gray-700 rounded-lg hover:border-gray-600 transition-colors">
                Связаться с нами
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Готовы пройти интервью?
          </h2>
          <p className="text-xl text-gray-400 mb-10">
            Присоединяйтесь к разработчикам, которые уже используют Hintsage
          </p>
          <Link href="/register" className="bg-white text-black px-8 py-4 rounded-lg font-medium hover:bg-gray-100 transition-colors inline-flex items-center gap-2">
            Начать бесплатно
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-12 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-gray-400 text-sm mb-4 md:mb-0">
              © 2025 Hintsage. Все права защищены.
            </div>
            <div className="flex space-x-6">
              <Link href="/login" className="text-gray-400 hover:text-white text-sm transition-colors">
                Войти
              </Link>
              <Link href="/register" className="text-gray-400 hover:text-white text-sm transition-colors">
                Регистрация
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
