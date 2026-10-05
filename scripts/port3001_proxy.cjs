const http = require('http');
const net = require('net');

const server = http.createServer((req, res) => {
  const options = {
    hostname: '127.0.0.1',
    port: 3000,
    path: req.url,
    method: req.method,
    headers: { ...req.headers, host: 'localhost:3000' }
  };

  const proxyReq = http.request(options, (proxyRes) => {
    res.writeHead(proxyRes.statusCode, proxyRes.headers);
    proxyRes.pipe(res, { end: true });
  });

  proxyReq.on('error', (err) => {
    res.writeHead(502);
    res.end('Proxy error: ' + err.message);
  });

  req.pipe(proxyReq, { end: true });
});

server.on('upgrade', (req, socket, head) => {
  socket.on('error', () => {});

  const proxySocket = net.connect(3000, '127.0.0.1', () => {
    proxySocket.write(`${req.method} ${req.url} HTTP/1.1\r\n`);
    for (const [key, value] of Object.entries(req.headers)) {
      if (key.toLowerCase() === 'host') {
        proxySocket.write(`host: localhost:3000\r\n`);
      } else {
        proxySocket.write(`${key}: ${value}\r\n`);
      }
    }
    proxySocket.write('\r\n');
    if (head && head.length > 0) proxySocket.write(head);
    socket.pipe(proxySocket).pipe(socket);
  });

  proxySocket.on('error', () => {
    socket.destroy();
  });
});

process.on('uncaughtException', (err) => {
  if (err.code === 'ECONNRESET' || err.code === 'EPIPE') return;
  console.error('Unhandled exception:', err);
});

server.listen(3001, () => {
  console.log('Port 3001 proxy running -> forwards to 3000');
});
