'use strict';
// Local preview that behaves like the Vercel deployment:
//   npm run dev                      -> http://localhost:3000
//   MOCK_SERVICES=1 npm run dev      -> online form works with fake Turnstile/Supabase/Resend
// Reads optional settings from .env.local (never commit that file).

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const dist = path.join(root, 'dist');
const port = Number(process.env.PORT || 3000);

// Minimal .env.local loader
const envFile = path.join(root, '.env.local');
if (fs.existsSync(envFile)) {
  for (const line of fs.readFileSync(envFile, 'utf8').split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
}

if (process.env.MOCK_SERVICES === '1') {
  Object.assign(process.env, {
    SUPABASE_URL: process.env.SUPABASE_URL || 'https://mock.supabase.co',
    SUPABASE_SECRET_KEY: process.env.SUPABASE_SECRET_KEY || 'mock',
    TURNSTILE_SECRET_KEY: process.env.TURNSTILE_SECRET_KEY || 'mock',
    TURNSTILE_SITE_KEY: process.env.TURNSTILE_SITE_KEY || '1x00000000000000000000AA',
    SITE_HOSTNAME: process.env.SITE_HOSTNAME || 'localhost'
  });
  const realFetch = global.fetch;
  global.fetch = async (url, opts = {}) => {
    const u = String(url);
    if (u.includes('turnstile/v0/siteverify')) {
      const token = new URLSearchParams(String(opts.body)).get('response');
      return { ok: true, json: async () => ({ success: Boolean(token), hostname: 'localhost', action: 'enquiry' }) };
    }
    if (u.includes('/rest/v1/enquiries')) {
      if (opts.method === 'POST') console.log('[mock supabase] stored enquiry:', opts.body);
      if (process.env.MOCK_STORE_FAIL === '1') return { ok: false, status: 503 };
      return { ok: true, status: 201, json: async () => [] };
    }
    if (u.includes('api.resend.com')) { console.log('[mock resend] email:', JSON.parse(opts.body).subject); return { ok: true }; }
    return realFetch(url, opts);
  };
  console.log('MOCK_SERVICES on: Turnstile, Supabase and Resend calls are simulated.');
}

const vercel = JSON.parse(fs.readFileSync(path.join(root, 'vercel.json'), 'utf8'));
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2', '.txt': 'text/plain', '.xml': 'application/xml' };

function applyHeaders(res, urlPath) {
  for (const rule of vercel.headers || []) {
    const re = new RegExp('^' + rule.source.replace('(.*)', '.*') + '$');
    if (re.test(urlPath)) for (const h of rule.headers) {
      // Local http cannot upgrade to https; drop that directive locally.
      res.setHeader(h.key, h.key === 'Content-Security-Policy' ? h.value.replace('; upgrade-insecure-requests', '') : h.value);
    }
  }
}

function wrapResponse(res) {
  res.status = code => { res.statusCode = code; return res; };
  res.json = body => { if (!res.getHeader('Content-Type')) res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(body)); return res; };
  return res;
}

async function runFunction(name, req, res) {
  const file = path.join(root, 'api', `${name}.js`);
  if (!/^[a-z0-9-]+$/.test(name) || !fs.existsSync(file)) return false;
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const raw = Buffer.concat(chunks).toString('utf8');
  let parsed;
  Object.defineProperty(req, 'body', {
    configurable: true,
    get() {
      if (parsed !== undefined) return parsed;
      if (!raw) return (parsed = undefined);
      if (String(req.headers['content-type'] || '').includes('application/json')) return (parsed = JSON.parse(raw)); // throws like Vercel
      return (parsed = raw);
    }
  });
  try {
    await require(file)(req, wrapResponse(res));
  } catch (err) {
    console.error(err);
    if (!res.headersSent) res.statusCode = 500;
    res.end();
  }
  return true;
}

function serveFile(res, file, status = 200) {
  res.statusCode = status;
  res.setHeader('Content-Type', TYPES[path.extname(file)] || 'application/octet-stream');
  fs.createReadStream(file).pipe(res);
}

http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const p = decodeURIComponent(url.pathname);
  applyHeaders(res, p);
  if (p.startsWith('/api/')) {
    if (await runFunction(p.slice(5).replace(/\/$/, ''), req, res)) return;
  }
  const candidates = p.endsWith('/') ? [path.join(dist, p, 'index.html')] : [path.join(dist, p), path.join(dist, `${p}.html`)];
  for (const file of candidates) {
    if (file.startsWith(dist) && fs.existsSync(file) && fs.statSync(file).isFile()) return serveFile(res, file);
  }
  serveFile(res, path.join(dist, '404.html'), 404);
}).listen(port, () => console.log(`SVI website on http://localhost:${port}`));
