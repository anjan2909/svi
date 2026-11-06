'use strict';

// Shared server-side configuration helpers. Nothing here is sent to the browser
// except the public Turnstile site key (see api/form-config.js).

const REQUIRED = ['SUPABASE_URL', 'SUPABASE_SECRET_KEY', 'TURNSTILE_SECRET_KEY', 'TURNSTILE_SITE_KEY', 'SITE_HOSTNAME'];

function missingConfig(env = process.env) {
  return REQUIRED.filter(key => !String(env[key] || '').trim());
}

// SITE_HOSTNAME may hold one hostname or a comma-separated list, e.g.
// "svicontrolpanel.com,www.svicontrolpanel.com,svi-website.vercel.app".
function allowedHostnames(env = process.env) {
  return String(env.SITE_HOSTNAME || '')
    .split(',')
    .map(h => h.trim().toLowerCase().replace(/^https?:\/\//, '').replace(/\/.*$/, ''))
    .filter(Boolean);
}

function supabaseBase(env = process.env) {
  return String(env.SUPABASE_URL || '').trim().replace(/\/+$/, '');
}

function supabaseHeaders(env = process.env) {
  // New-style secret keys (sb_secret_...) go in the apikey header only.
  return { apikey: env.SUPABASE_SECRET_KEY, 'Content-Type': 'application/json' };
}

module.exports = { REQUIRED, missingConfig, allowedHostnames, supabaseBase, supabaseHeaders };
