'use strict';

const { test, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const handler = require('../api/enquiry');
const formConfig = require('../api/form-config');
const keepAlive = require('../api/keep-alive');

const ENV = {
  SUPABASE_URL: 'https://example.supabase.co/',
  SUPABASE_SECRET_KEY: 'sb_secret_test',
  TURNSTILE_SECRET_KEY: 'ts_secret_test',
  TURNSTILE_SITE_KEY: 'ts_site_test',
  SITE_HOSTNAME: 'svicontrolpanel.com, www.svicontrolpanel.com'
};
const ALL_KEYS = [...Object.keys(ENV), 'RESEND_API_KEY', 'NOTIFY_EMAIL_TO', 'NOTIFY_EMAIL_FROM', 'CRON_SECRET'];

let savedEnv, savedFetch, calls;
beforeEach(() => {
  savedEnv = Object.fromEntries(ALL_KEYS.map(k => [k, process.env[k]]));
  savedFetch = global.fetch;
  ALL_KEYS.forEach(k => delete process.env[k]);
  calls = [];
});
afterEach(() => {
  ALL_KEYS.forEach(k => (savedEnv[k] === undefined ? delete process.env[k] : (process.env[k] = savedEnv[k])));
  global.fetch = savedFetch;
});

const res = () => ({ headers: {}, setHeader(k, v) { this.headers[k] = v; }, status(n) { this.code = n; return this; }, json(b) { this.body = b; return this; } });
const goodBody = () => ({
  name: 'Test User', email: 'Test@Example.com', phone: '+91 98251 08477', company: 'Test Co',
  panel_type: 'MCC panel', message: 'Please quote an MCC panel for 12 motors.', consent: true, token: 'tok'
});
const post = body => ({ method: 'POST', headers: { 'content-type': 'application/json' }, body });

function mockFetch({ verify = { success: true, hostname: 'www.svicontrolpanel.com', action: 'enquiry' }, store = true, mail = true } = {}) {
  global.fetch = async (url, opts = {}) => {
    calls.push({ url: String(url), opts });
    if (String(url).includes('siteverify')) return { json: async () => verify };
    if (String(url).includes('resend.com')) { if (mail === 'throw') throw new Error('down'); return { ok: mail }; }
    return { ok: store };
  };
}

test('rejects wrong method, wrong content type and malformed JSON', async () => {
  let r = res(); await handler({ method: 'GET', headers: {} }, r); assert.equal(r.code, 405);
  r = res(); await handler({ method: 'POST', headers: { 'content-type': 'text/plain' }, body: 'x' }, r); assert.equal(r.code, 415);
  const req = { method: 'POST', headers: { 'content-type': 'application/json' } };
  Object.defineProperty(req, 'body', { get() { throw new SyntaxError('bad json'); } });
  r = res(); await handler(req, r); assert.equal(r.code, 400);
  r = res(); await handler(post([1, 2]), r); assert.equal(r.code, 400);
});

test('validates fields, consent, phone digits and the bot trap', async () => {
  for (const patch of [{ name: 'A' }, { email: 'nope' }, { phone: '---------' }, { phone: '12345' }, { message: 'too short' },
    { consent: 'true' }, { panel_type: 'Rocket' }, { website: 'spam.example' }]) {
    const r = res(); await handler(post({ ...goodBody(), ...patch }), r);
    assert.equal(r.code, 400, JSON.stringify(patch));
  }
  assert.equal(calls.length, 0);
});

test('reports "not switched on" when configuration is missing', async () => {
  const r = res(); await handler(post(goodBody()), r);
  assert.equal(r.code, 503);
  assert.match(r.body.error, /not switched on/);
});

test('requires a passing challenge for an allowed hostname and action', async () => {
  Object.assign(process.env, ENV);
  for (const verify of [{ success: false }, { success: true, hostname: 'evil.example', action: 'enquiry' }, { success: true, hostname: 'svicontrolpanel.com', action: 'login' }]) {
    calls = []; mockFetch({ verify });
    const r = res(); await handler(post(goodBody()), r);
    assert.equal(r.code, 400); assert.equal(calls.length, 1);
  }
});

test('stores a cleaned enquiry and only reports success after the database accepts it', async () => {
  Object.assign(process.env, ENV);
  mockFetch();
  let r = res(); await handler(post({ ...goodBody(), name: '  Test   User ' }), r);
  assert.equal(r.code, 201); assert.deepEqual(r.body, { ok: true });
  const insert = calls.find(c => c.url.includes('/rest/v1/enquiries'));
  assert.equal(insert.url, 'https://example.supabase.co/rest/v1/enquiries');
  assert.equal(insert.opts.headers.apikey, 'sb_secret_test');
  assert.deepEqual(JSON.parse(insert.opts.body), { name: 'Test User', email: 'test@example.com', phone: '+91 98251 08477', company: 'Test Co', panel_type: 'MCC panel', message: 'Please quote an MCC panel for 12 motors.' });
  assert.ok(!calls.some(c => c.url.includes('resend.com')), 'no email unless configured');

  mockFetch({ store: false });
  r = res(); await handler(post(goodBody()), r); assert.equal(r.code, 503);
});

test('emails the owner when configured, and a mail failure never loses the enquiry', async () => {
  Object.assign(process.env, ENV, { RESEND_API_KEY: 're_test', NOTIFY_EMAIL_TO: 'owner@example.com, sales@example.com' });
  for (const mail of [true, false, 'throw']) {
    calls = []; mockFetch({ mail });
    const r = res(); await handler(post(goodBody()), r);
    assert.equal(r.code, 201, `mail=${mail}`);
  }
  const email = JSON.parse(calls.find(c => c.url.includes('resend.com')).opts.body);
  assert.deepEqual(email.to, ['owner@example.com', 'sales@example.com']);
  assert.equal(email.reply_to, 'test@example.com');
  assert.match(email.text, /MCC panel/);
});

test('form-config exposes readiness and the public key only', async () => {
  let r = res(); formConfig({ method: 'GET' }, r);
  assert.deepEqual(r.body, { ready: false, siteKey: null });
  Object.assign(process.env, ENV);
  r = res(); formConfig({ method: 'GET' }, r);
  assert.deepEqual(r.body, { ready: true, siteKey: 'ts_site_test' });
  assert.ok(!JSON.stringify(r.body).includes('secret'));
  r = res(); formConfig({ method: 'POST' }, r); assert.equal(r.code, 405);
});

test('keep-alive needs the cron secret and touches the database', async () => {
  Object.assign(process.env, ENV);
  let r = res(); await keepAlive({ headers: {} }, r); assert.equal(r.code, 503);
  process.env.CRON_SECRET = 'cron123';
  r = res(); await keepAlive({ headers: { authorization: 'Bearer wrong' } }, r); assert.equal(r.code, 401);
  mockFetch();
  r = res(); await keepAlive({ headers: { authorization: 'Bearer cron123' } }, r);
  assert.equal(r.code, 200);
  assert.equal(calls[0].url, 'https://example.supabase.co/rest/v1/enquiries?select=id&limit=1');
});
