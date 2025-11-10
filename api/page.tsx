// app/page.tsx - نسخه به‌روز شده
'use client'
import { useState, useEffect } from 'react'

const API_BASE = "https://tetrashop-mpshbs48g-ramin-edjlal-s-projects.vercel.app"

export default function Home() {
  const [healthStatus, setHealthStatus] = useState<any>(null)
  const [sessionData, setSessionData] = useState<any>(null)

  const testHealth = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/health`)
      const data = await response.json()
      setHealthStatus(data)
    } catch (error) {
      setHealthStatus({ error: 'خطا در اتصال به API' })
    }
  }

  const createSession = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/sessions/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          user_id: 'user_' + Date.now(),
          context: { platform: 'web' }
        })
      })
      const data = await response.json()
      setSessionData(data)
    } catch (error) {
      setSessionData({ error: 'خطا در ایجاد سشن' })
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100" dir="rtl">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">🚀 تتراشاپ - پنل مدیریت</h1>
        
        {/* کارت‌های آماری */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl font-semibold mb-2">💰 درآمد امروز</h3>
            <p className="text-3xl font-bold text-green-600">۲,۵۰۰,۰۰۰ تومان</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl font-semibold mb-2">👥 کاربران فعال</h3>
            <p className="text-3xl font-bold text-blue-600">۱,۲۴۳ نفر</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl font-semibold mb-2">🏪 محصولات</h3>
            <p className="text-3xl font-bold text-purple-600">۸۷ عدد</p>
          </div>
        </div>

        {/* اتصال به API */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h2 className="text-2xl font-bold mb-4">🔗 اتصال به API تتراشاپ</h2>
          
          <div className="space-y-4">
            <button 
              onClick={testHealth}
              className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600"
            >
              تست سلامت API
            </button>
            
            <button 
              onClick={createSession}
              className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600"
            >
              ایجاد سشن جدید
            </button>
          </div>

          {/* نتایج */}
          {healthStatus && (
            <div className="mt-4 p-4 bg-gray-100 rounded">
              <h3 className="font-semibold">نتایج سلامت API:</h3>
              <pre>{JSON.stringify(healthStatus, null, 2)}</pre>
            </div>
          )}

          {sessionData && (
            <div className="mt-4 p-4 bg-gray-100 rounded">
              <h3 className="font-semibold">نتایج ایجاد سشن:</h3>
              <pre>{JSON.stringify(sessionData, null, 2)}</pre>
            </div>
          )}
        </div>

        {/* درگاه پرداخت نمونه */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4">💳 درگاه پرداخت آزمایشی</h2>
          <button className="bg-purple-500 text-white px-6 py-3 rounded-lg hover:bg-purple-600">
            پرداخت ۱۰,۰۰۰ تومان
          </button>
        </div>
      </div>
    </div>
  )
        }
