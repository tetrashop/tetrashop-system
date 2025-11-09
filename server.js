import http from 'http';
import { handler } from './api/index.js';

const server = http.createServer(async (req, res) => {
  // اضافه کردن CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  await handler(req, res);
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`🚀 Tetrashop API Server running on http://localhost:${PORT}`);
  console.log('📊 Endpoints:');
  console.log('   GET  /api/health');
  console.log('   POST /api/v1/sessions/create');
  console.log('   GET  /api');
});
