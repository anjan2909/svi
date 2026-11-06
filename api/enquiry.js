'use strict';

const { missingConfig, allowedHostnames, supabaseBase, supabaseHeaders } = require('../lib/config');

const PANEL_TYPES = new Set([
  '', 'PCC panel', 'MCC panel', 'PLC / automation panel', 'AMF / synchronizing panel',
  'APFC / harmonic filter panel', 'Bus duct / distribution', 'Other / not sure'
]);

const clean = value => (typeof value === 'string' ? value.replace(/\s+/g, ' ').trim() : '');
const cleanMessage = value => (typeof value === 'string' ? value.replace(/\r\n?/g, '\n').trim() : '');

function validate(body) {
  const data = {
    name: clean(body.name),
    email: clean(body.email).toLowerCase(),
    phone: clean(body.phone),
    company: clean(body.company),
    panel_type: clean(body.panel_type),
    message: cleanMessage(body.message)
  };
  const digits = data.phone.replace(/\D/g, '').length;
  const ok =
    data.name.length >= 2 && data.name.length <= 100 &&
    data.email.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email) &&
    /^[+()\d\s.-]{7,30}$/.test(data.phone) && digits >= 7 && digits <= 15 &&
    data.company.length <= 150 &&
    PANEL_TYPES.has(data.panel_type) &&
    data.message.length >= 20 && data.message.length <= 5000 &&
    body.consent === true;
  return ok ? data : null;
}

async function notifyOwner(data) {
  // Optional: email the owner about each new enquiry through Resend.
  // Switched on only when RESEND_API_KEY and NOTIFY_EMAIL_TO are both set.
  const { RESEND_API_KEY, NOTIFY_EMAIL_TO, NOTIFY_EMAIL_FROM } = process.env;
  if (!RESEND_API_KEY || !NOTIFY_EMAIL_TO) return 'skipped';
  const lines = [
    `Name: ${data.name}`,
    `Email: ${data.email}`,
    `Phone: ${data.phone}`,
    `Company: ${data.company || '-'}`,
    `Panel type: ${data.panel_type || '-'}`,
    '',
    data.message,
    '',
    'This enquiry is also saved in Supabase (Table Editor > enquiries).'
  ];
  try {
    const sent = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: NOTIFY_EMAIL_FROM || 'SVI Website <onboarding@resend.dev>',
        to: NOTIFY_EMAIL_TO.split(',').map(s => s.trim()).filter(Boolean),
        reply_to: data.email,
        subject: `New website enquiry: ${data.name}${data.company ? ` (${data.company})` : ''}`,
        text: lines.join('\n')
      }),
      signal: AbortSignal.timeout(5000)
    });
    return sent.ok ? 'sent' : 'failed';
  } catch {
    return 'failed';
  }
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed.' });
  }
  if (!String((req.headers && req.headers['content-type']) || '').includes('application/json')) {
    return res.status(415).json({ error: 'JSON required.' });
  }

  let body;
  try {
    body = req.body; // Vercel parses JSON lazily and throws on malformed input.
  } catch {
    return res.status(400).json({ error: 'Invalid enquiry.' });
  }
  if (!body || typeof body !== 'object' || Array.isArray(body) || Buffer.byteLength(JSON.stringify(body)) > 12000) {
    return res.status(400).json({ error: 'Invalid enquiry.' });
  }
  if (body.website) return res.status(400).json({ error: 'Unable to accept this enquiry.' }); // bot trap

  const data = validate(body);
  if (!data) return res.status(400).json({ error: 'Please check your contact details, message, and consent.' });

  if (missingConfig().length) {
    return res.status(503).json({ error: 'Online enquiries are not switched on yet. Please use WhatsApp, email or phone.' });
  }

  try {
    const check = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      body: new URLSearchParams({ secret: process.env.TURNSTILE_SECRET_KEY, response: typeof body.token === 'string' ? body.token : '' }),
      signal: AbortSignal.timeout(8000)
    });
    const verification = await check.json();
    const hostOk = allowedHostnames().includes(String(verification.hostname || '').toLowerCase());
    if (!verification.success || !hostOk || verification.action !== 'enquiry') {
      return res.status(400).json({ error: 'Security check failed. Please complete it again and resend.' });
    }

    const saved = await fetch(`${supabaseBase()}/rest/v1/enquiries`, {
      method: 'POST',
      headers: { ...supabaseHeaders(), Prefer: 'return=minimal' },
      body: JSON.stringify(data),
      signal: AbortSignal.timeout(8000)
    });
    if (!saved.ok) throw new Error('Storage unavailable');
  } catch {
    return res.status(503).json({ error: 'We could not confirm delivery. Please try again, or send it on WhatsApp or email.' });
  }

  await notifyOwner(data); // best effort: the enquiry is already stored
  return res.status(201).json({ ok: true });
};

module.exports.validate = validate;
module.exports.PANEL_TYPES = PANEL_TYPES;
