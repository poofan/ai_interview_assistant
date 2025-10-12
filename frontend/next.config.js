/** @type {import('next').NextConfig} */
const nextConfig = {
  // Настройки для правильной работы с UTF-8
  webpack: (config) => {
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
    }
    return config
  },
  // Отключаем строгий режим для совместимости
  reactStrictMode: false,
}

module.exports = nextConfig
