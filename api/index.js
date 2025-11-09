// API Handler برای Vercel
module.exports = async (req, res) => {
  // تنظیم CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  // هندل کردن OPTIONS برای CORS preflight
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  
  const { pathname } = new URL(req.url, `http://${req.headers.host}`);
  
  console.log(`📥 ${req.method} request to: ${pathname}`);
  
  try {
    // مسیر سلامت
    if (pathname === '/api/health' || pathname === '/api/v1/health') {
      return res.status(200).json({
        status: "healthy",
        service: "Tetrashop API",
        timestamp: Date.now(),
        environment: process.env.NODE_ENV || "production",
        version: "1.0.0"
      });
    }
    
    // ایجاد سشن
    if (pathname === '/api/v1/sessions/create' && req.method === 'POST') {
      let body = '';
      req.on('data', chunk => {
        body += chunk.toString();
      });
      
      req.on('end', () => {
        try {
          const data = JSON.parse(body);
          return res.status(200).json({
            status: "success",
            session_id: `session_${Date.now()}_${data.user_id || 'anonymous'}`,
            user_id: data.user_id,
            created_at: Date.now(),
            message: "Session created successfully"
          });
        } catch (error) {
          return res.status(400).json({
            error: "Invalid JSON",
            message: error.message
          });
        }
      });
      return;
    }
    
    // صفحه اصلی API
    if (pathname === '/api' || pathname === '/') {
      return res.status(200).json({
        message: "🚀 Tetrashop Adaptive System API",
        status: "active", 
        version: "4.0.0",
        github: "https://github.com/tetrashop/tetrashop-system",
        endpoints: {
          "GET /api/health": "Health check",
          "POST /api/v1/sessions/create": "Create session",
          "GET /api": "API information"
        }
      });
    }
    
    // خطای 404
    res.status(404).json({
      error: "Endpoint not found",
      path: pathname,
      method: req.method,
      available_endpoints: ["/api/health", "/api/v1/sessions/create", "/api"]
    });
    
  } catch (error) {
    console.error('❌ Server error:', error);
    res.status(500).json({
      error: "Internal server error",
      message: error.message
    });
  }
};
