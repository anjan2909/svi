'use strict';

const { supabaseBase, supabaseHeaders } = require('../lib/config');

// Daily Vercel cron (see vercel.json). Supabase pauses Free-plan projects that
// see too little database activity in a week; a paused project would make the
// enquiry form fail. This makes one tiny read so the project stays active.
// Vercel sends "Authorization: Bearer <CRON_SECRET>" when CRON_SECRET is set.
module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  const secret = process.env.CRON_SECRET;
  if (!secret) return res.status(503).json({ error: 'CRON_SECRET is not configured.' });
  if (((req.headers && req.headers.authorization) || '') !== `Bearer ${secret}`) {
    return res.status(401).json({ error: 'Unauthorized.' });
  }
  if (!process.env.SUPABASE_URL || !process.env.SUPABASE_SECRET_KEY) {
    return res.status(503).json({ error: 'Database is not configured.' });
  }
  try {
    const r = await fetch(`${supabaseBase()}/rest/v1/enquiries?select=id&limit=1`, {
      headers: supabaseHeaders(),
      signal: AbortSignal.timeout(8000)
    });
    if (!r.ok) throw new Error(String(r.status));
    return res.status(200).json({ ok: true });
  } catch {
    return res.status(502).json({ ok: false, error: 'Database did not respond.' });
  }
};
