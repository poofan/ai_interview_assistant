import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Hintsage - AI Interview Assistant',
  description: 'Умный ассистент для технических интервью с real-time подсказками на базе AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      <body>{children}</body>
    </html>
  )
}
