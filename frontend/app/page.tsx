import Link from 'next/link'
import { ArrowRight, Zap, Shield, Cpu, CheckCircle } from 'lucide-react'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900">
      {/* Navigation */}
      <nav className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm fixed w-full z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
                Hintsage
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/login" className="text-gray-300 hover:text-white transition">
                Вход
              </Link>
              <Link href="/register" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition">
                Начать
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
            AI Ассистент для
            <span className="block bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
              Технических Интервью
            </span>
          </h1>
          <p className="text-xl text-gray-400 mb-8 max-w-3xl mx-auto">
            Hintsage помогает вам уверенно проходить технические интервью с помощью
            real-time подсказок на базе AI
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/register" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-lg font-semibold flex items-center gap-2 transition">
              Начать бесплатно
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link href="#pricing" className="border border-gray-700 hover:border-gray-600 text-white px-8 py-4 rounded-lg text-lg font-semibold transition">
              Цены
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-12">
            Мощные возможности
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<Zap className="w-8 h-8 text-blue-500" />}
              title="GPU Ускорение"
              description="Whisper STT с поддержкой CUDA для мгновенного распознавания речи"
            />
            <FeatureCard
              icon={<Shield className="w-8 h-8 text-purple-500" />}
              title="Полная Конфиденциальность"
              description="Антидетект защита от скриншотов и захвата экрана"
            />
            <FeatureCard
              icon={<Cpu className="w-8 h-8 text-green-500" />}
              title="AI Подсказки"
              description="GPT-4 анализирует вопросы и дает точные ответы в реальном времени"
            />
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-20 px-4 bg-gray-900/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-white text-center mb-12">
            Выберите свой план
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <PricingCard
              name="Free"
              price="0"
              period="навсегда"
              features={[
                "Базовый STT (Vosk)",
                "5 запросов/час",
                "Стандартный контекст"
              ]}
              cta="Начать бесплатно"
              ctaLink="/register"
            />
            <PricingCard
              name="Pro"
              price="1 499"
              period="/ месяц"
              features={[
                "Whisper GPU STT",
                "Безлимитные запросы",
                "Расширенный контекст",
                "Кастомные промпты",
                "OCR скриншотов",
                "Приоритетная поддержка"
              ]}
              cta="Купить Pro"
              ctaLink="/register"
              popular={true}
            />
            <PricingCard
              name="Enterprise"
              price="7 490"
              period="/ месяц"
              features={[
                "Все из Pro",
                "Командный доступ",
                "Кастомные интеграции",
                "Выделенная поддержка",
                "SLA гарантии"
              ]}
              cta="Связаться с нами"
              ctaLink="/register"
            />
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Готовы пройти интервью с уверенностью?
          </h2>
          <Link href="/register" className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition">
            Начать сейчас
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-8 px-4">
        <div className="max-w-7xl mx-auto text-center text-gray-500">
          <p>&copy; 2025 Hintsage. Все права защищены.</p>
        </div>
      </footer>
    </main>
  )
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-6 hover:border-gray-600 transition">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-gray-400">{description}</p>
    </div>
  )
}

function PricingCard({ 
  name, 
  price, 
  period, 
  features, 
  cta, 
  ctaLink, 
  popular 
}: { 
  name: string; 
  price: string; 
  period: string; 
  features: string[]; 
  cta: string; 
  ctaLink: string; 
  popular?: boolean 
}) {
  return (
    <div className={`bg-gray-800/50 border ${popular ? 'border-blue-500' : 'border-gray-700'} rounded-xl p-8 relative`}>
      {popular && (
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
          <span className="bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
            Популярный
          </span>
        </div>
      )}
      <h3 className="text-2xl font-bold text-white mb-2">{name}</h3>
      <div className="mb-6">
        <span className="text-4xl font-bold text-white">{price} ₽</span>
        <span className="text-gray-400 ml-2">{period}</span>
      </div>
      <ul className="space-y-3 mb-8">
        {features.map((feature, i) => (
          <li key={i} className="flex items-start gap-2 text-gray-300">
            <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
            <span>{feature}</span>
          </li>
        ))}
      </ul>
      <Link href={ctaLink} className={`block text-center py-3 rounded-lg font-semibold transition ${
        popular 
          ? 'bg-blue-600 hover:bg-blue-700 text-white' 
          : 'border border-gray-700 hover:border-gray-600 text-white'
      }`}>
        {cta}
      </Link>
    </div>
  )
}
