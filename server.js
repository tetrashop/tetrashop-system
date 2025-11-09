const http = require('http');
const handler = require('./api/index.js');

const server = http.createServer(async (req, res) => {
  await handler(req, res);
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`🚀 Tetrashop API Server running on http://localhost:${PORT}`);
  console.log('📊 Available endpoints:');
  console.log('   GET  /api/health');
  console.log('   POST /api/v1/sessions/create'); 
  console.log('   GET  /api');
  console.log('⏹️  Press Ctrl+C to stop');
});
