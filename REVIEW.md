# SVI website — review and changes (5 Nov 2026)

Review of the hand-over package (`svi-vercel-supabase.zip`, `SVI-handoff.md`,
`SVI-Complete-Handover.html`) and the earlier static build (`svi-control-panel-site.tar.gz`,
same design without the form). The earlier ChatGPT preview link could not be opened from here
and is superseded.

**Overall:** a good-looking, sensible base. The design, copy and server approach were sound.
The problems were mainly in how the form behaves in real life, page weight, and launch basics.
Everything below marked *Fixed* is done in this package and covered by 8 server tests and
52 browser checks (desktop, tablet, phone, reduced motion, no JavaScript). The live services were simulated in testing; a real
end-to-end test after deployment is still required.

## Fixed

| # | Issue found | Impact | What changed |
|---|---|---|---|
| 1 | Product grid left an empty grey block (two cells on desktop, one on tablet) | Looked broken in the main sales section | Added a "Custom builds — Start an enquiry" card that completes the grid at every width |
| 2 | Until all five cloud settings exist, the form was a dead end: visitors could fill it in but never send | Lost enquiries during setup and whenever a service fails | Form now works from day one by opening WhatsApp or email with the message pre-written; switches to online sending automatically once configured; if an online send fails it offers WhatsApp/email and keeps what was typed |
| 3 | Supabase pauses Free-plan projects with low activity over ~7 days | A quiet B2B form would silently start failing | Daily keep-alive job (`/api/keep-alive`, Vercel cron). Alternative: paid Supabase plan |
| 4 | No notification — leads only sit in a database table | Leads go unanswered | Optional email alert per enquiry via Resend (reply goes straight to the customer); never blocks saving |
| 5 | Malformed request made the function crash (500) | Noise in logs, unclear errors | Returns a clean 400 |
| 6 | Spam check accepted exactly one hostname | `www`, apex and preview URLs could not all work | `SITE_HOSTNAME` takes a comma-separated list |
| 7 | Phone check accepted "-------" | Junk leads | Requires 7–15 digits (browser and server) |
| 8 | Hero image was a 2 MB PNG | Slow first load, especially on mobile data | 105 KB WebP with smaller sizes for phones, JPEG fallback; total page ≈ 230 KB |
| 9 | Fonts loaded from Google | Extra third-party requests; slower | Fonts self-hosted |
| 10 | Copy asked visitors to "share your SLD, BOQ…" but the form has no attachments | Confusing promise | Copy now says drawings can follow by email/WhatsApp after the reply |
| 11 | Sending disabled the button, which threw keyboard focus to the top of the page | Accessibility | Button shows a busy state without losing focus; menu closes with Esc; contrast checked |
| 12 | No favicon, link-preview image, canonical URL, business structured data, robots/sitemap, 404 or privacy page | Weak search/social presence; consent text had no notice to point to | All added (privacy notice is a draft — see below) |
| 13 | Only two basic security headers | — | Added Content-Security-Policy, HSTS, Permissions-Policy, frame blocking |
| 14 | Node version range `>=22` | Unpredictable runtime | Pinned to Node 24.x (Vercel's current default) |
| 15 | AI-generated hero could be read as an SVI installation | Misleading | Small "Illustrative image" label and honest alt text until real photos arrive |

### Also added
- **Illustrations (update, 5 Nov):** 13 original vector drawings in the site's style — each product
  card now shows its panel type (PCC, MCC, PLC, AMF/synchronizing, APFC, bus duct/feeder pillar);
  a new **Inside the workshop** gallery shows sheet-metal forming, welding, powder coating,
  busbars & wiring, testing and site commissioning; *Why SVI* shows a technician working inside a panel.
- **Motion and components (update, 5 Nov):** hero entrance with slow zoom, scroll reveals,
  hover lifts, reading-progress bar and gently glowing lamps in the drawings (all off for
  reduced-motion users). New **Inside every panel** grid of eight drawn components (ACB, MCCB,
  MCB/RCCB, contactor + overload relay, protection relay, PLC/HMI, meters, busbars); animated
  **counters**; an eight-question **FAQ**; a **customer reviews** slider kept hidden until real quotes exist.
- **Location (updated 7 Nov):** the owner's Google Maps pin (22.981963, 72.724989) drives the
  "Open in Google Maps" and "Get directions" links, a live Google map in the contact section with an
  address card over it (it loads as the visitor scrolls near it; privacy notice updated) and the
  coordinates in the search-engine data. If a page or browser blocks embedded maps, the drawn pin
  stays with a short note and the card's links still work.
- **Logo (8 Nov):** the owner's logo replaces the placeholder mark in the header, footer, browser-tab icon,
  phone home-screen icon, link-preview image and search-engine data.
- Every product card has **Enquire →**, which jumps to the form with the panel type pre-selected.
- Optional **Panel type** field (stored in a new `panel_type` column) and an internal `notes` column.
- Phone/tablet **Call · WhatsApp · Get a quote** bar (appears after the hero, hides at the form).
- Two-column form on desktop; "Phone / WhatsApp" label; clearer success and error messages.
- `npm run dev` local preview that mimics Vercel, with a `MOCK_SERVICES=1` mode to test online sending without accounts.

## Needs the owner

1. **Business identity.** Confirm the trading and legal names (SVI Control Panel / Siddhi Vinayak
   Industries), phone/WhatsApp, address and the 2009 founding year. Note: another panel maker
   in Bakrol–Bujrang also abbreviates to "SVI" (Shakti Vijay Industries), so consistent naming matters.
2. **Email address.** The site uses a personal Yahoo address. A domain address such as
   `enquiry@svicontrolpanel.com` looks more credible and is needed to send alerts from your own domain.
3. **Photos.** The new drawings make the site complete, but real photos of SVI's own
   panels, workshop and team will be more convincing to buyers. Send them when available and they
   can replace the drawings one by one. Also replace the AI hero image. (The official logo is in
   place since 8 Nov; on dark backgrounds it carries a thin white outline so the black diamond shows.)
4. **Numbers, reviews and FAQ answers.** Send real figures for *panels delivered* and
   *customers served* to switch those counters on; send two or three real customer quotes (with
   permission) to show the reviews slider; confirm the FAQ answers, especially lead time,
   inspection visits and warranty, and the line that components follow the customer's approved make list.
5. **Privacy notice.** Review the wording in `dist/privacy.html`, choose a retention period,
   and name who answers enquiries.
6. **Accounts and costs.** GitHub, Vercel (a paid team is required for commercial use), Supabase,
   Cloudflare, and optionally Resend — all in the owner's name. Confirm plan prices before subscribing.
7. **Primary domain.** Code assumes `svicontrolpanel.com` (no www). Tell the developer if `www` is preferred.

## Not done (by design or out of scope)

- No file uploads (drawings go by email/WhatsApp after first contact).
- No admin dashboard; Supabase Table Editor is the inbox.
- No analytics. If wanted later, choose a privacy-friendly option and update the privacy notice and CSP.
- Turnstile + hidden bot-trap field are the spam controls; no separate rate limiter.
