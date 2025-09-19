#!/usr/bin/env bash
set -euo pipefail
# Replace server.js with a fixed implementation (safe query parsing).
cat > server.js <<'JS'
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const configPath = process.env.CONFIG_PATH || path.join(__dirname, 'config.json');
const raw = fs.readFileSync(configPath, 'utf8');
const cfg = JSON.parse(raw);

const port = process.env.PORT || cfg.port || 3000;

const server = http.createServer((req, res) => {
  if (req.url.startsWith('/health')) {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('OK');
    return;
  }

  if (req.url.startsWith('/greet')) {
    // parse query safely using WHATWG URL
    const url = new URL(req.url, `http://localhost:${port}`);
    const name = url.searchParams.get('name') || cfg.defaultName;
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(JSON.stringify({ greeting: `Hello, ${name}!` }));
    return;
  }

  res.writeHead(404);
  res.end();
});

server.listen(port, '0.0.0.0', () => {
  console.log(`listening ${port}`);
});
JS

echo "server.js patched by solution.sh"