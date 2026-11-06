'use strict';

const { missingConfig } = require('../lib/config');

// Tells the browser whether online enquiries are switched on, and gives it the
// public Turnstile site key. Never returns secrets or which variables are missing.
module.exports = function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({ error: 'Method not allowed.' });
  }
  const ready = missingConfig().length === 0;
  return res.status(200).json({ ready, siteKey: ready ? process.env.TURNSTILE_SITE_KEY.trim() : null });
};
