export default async function handler(request, response) {
  const { pathname } = new URL(request.url, `http://${request.headers.host}`);
  
  console.log(`📥 Incoming request: ${request.method} ${pathname}`);
  
  // مسیر سلامت
  if (pathname === '/api/health' || pathname === '/api/v1/health') {
    return response.status(200).json({
      status: "healthy",
      service: "Tetrashop API",
      timestamp: Date.now(),
      environment: process.env.NODE_ENV || "production"
    });
  }
  
  // ایجاد سشن
  if (pathname === '/api/v1/sessions/create' && request.method === 'POST') {
    try {
      const body = await readBody(request);
      const data = JSON.parse(body);
      
      return response.status(200).json({
        status: "success",
        session_id: `session_${Date.now()}_${data.user_id || 'anonymous'}`,
        user_id: data.user_id,
        created_at: Date.now(),
        message: "Session created successfully"
      });
    } catch (error) {
      return response.status(400).json({
        error: "Invalid JSON",
        message: error.message
      });
    }
  }
  
  // صفحه اصلی
  if (pathname === '/api' || pathname === '/') {
    return response.status(200).json({
      message: "🚀 Tetrashop Adaptive System API",
      status: "active",
      version: "4.0.0",
      endpoints: {
        "GET /api/health": "Health check",
        "POST /api/v1/sessions/create": "Create session",
        "GET /api": "API info"
      }
    });
  }
  
  // خطای 404 برای مسیرهای ناشناخته
  return response.status(404).json({
    error: "Endpoint not found",
    path: pathname,
    method: request.method
  });
}

// تابع برای خواندن body request
function readBody(request) {
  return new Promise((resolve, reject) => {
    let body = '';
    request.on('data', chunk => {
      body += chunk.toString();
    });
    request.on('end', () => {
      resolve(body);
    });
    request.on('error', reject);
  });
}
