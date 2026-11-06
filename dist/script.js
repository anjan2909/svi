(() => {
  'use strict';

  /* ---------- Header & menu ---------- */
  const header = document.querySelector('[data-header]');
  const menuButton = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('[data-nav]');

  const updateHeader = () => header.classList.toggle('scrolled', window.scrollY > 20);
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  const setMenu = open => {
    nav.classList.toggle('open', open);
    header.classList.toggle('menu-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  };
  menuButton.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); menuButton.focus(); }
  });
  document.addEventListener('click', e => {
    if (nav.classList.contains('open') && !header.contains(e.target)) setMenu(false);
  });

  const year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- Mobile quick-contact bar ----------
     Shown once the visitor has scrolled past most of the hero (which has its own
     call to action) and hidden again while the contact section is on screen. */
  const quick = document.querySelector('[data-quick]');
  const hero = document.querySelector('.hero');
  const contact = document.querySelector('#contact');
  if (quick && hero && contact) {
    let contactVisible = false;
    const updateQuick = () => quick.classList.toggle('is-hidden', contactVisible || window.scrollY < hero.offsetHeight * 0.6);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(([entry]) => { contactVisible = entry.isIntersecting; updateQuick(); }, { threshold: 0.05 }).observe(contact);
    }
    window.addEventListener('scroll', updateQuick, { passive: true });
    updateQuick();
  }

  /* ---------- Motion ---------- */
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Scroll progress bar and a gentle hero parallax (one update per frame).
  const bar = document.querySelector('[data-progress]');
  const heroPic = document.querySelector('.hero picture');
  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      if (bar) bar.style.transform = `scaleX(${max > 0 ? Math.min(1, window.scrollY / max) : 0})`;
      if (heroPic && !reduceMotion && window.scrollY < window.innerHeight * 1.2) {
        heroPic.style.transform = `translate3d(0, ${(window.scrollY * 0.25).toFixed(1)}px, 0)`;
      }
      ticking = false;
    });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Reveal content as it scrolls into view, children of each group one after another.
  if (!reduceMotion && 'IntersectionObserver' in window) {
    const groups = ['.section-head', '.intro-grid', '.stats', '.product-grid', '.parts-head', '.parts-grid', '.cap-top', '.steps',
      '.workshop-head', '.work-grid', '.industries-grid', '.industry-list', '.reviews-head', '.reviews-track',
      '.quality-grid', '.quality-points', '.faq-head', '.faq-list', '.contact-grid'];
    const io = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      io.unobserve(el);
      el.classList.add('is-in');
      const delay = (parseFloat(el.style.getPropertyValue('--d')) || 0) * 90;
      setTimeout(() => { el.classList.remove('reveal', 'is-in'); el.style.removeProperty('--d'); }, 1000 + delay);
    }), { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    const seen = new Set();
    groups.forEach(sel => document.querySelectorAll(sel).forEach(group => {
      // A sideways-scrolling row (gallery on phones) is revealed as one block.
      const sideways = ['auto', 'scroll'].includes(getComputedStyle(group).overflowX);
      (sideways ? [group] : [...group.children]).forEach((el, i) => {
        if (el.hidden || seen.has(el) || el.closest('[hidden]') || el.matches('.industry-list, .quality-points, .parts-head, .faq-head, .faq-list')) return;
        seen.add(el);
        el.classList.add('reveal');
        el.style.setProperty('--d', String(Math.min(i, 8)));
        io.observe(el);
      });
    }));
  }

  // Counters: final value is in the HTML; count up to it when first seen.
  document.querySelectorAll('[data-count]').forEach(el => {
    const raw = el.dataset.count;
    const target = raw.startsWith('since:') ? new Date().getFullYear() - parseInt(raw.slice(6), 10) : parseInt(raw, 10);
    if (!Number.isFinite(target)) return;
    el.textContent = target.toLocaleString('en-IN');
    if (reduceMotion || !('IntersectionObserver' in window) || el.closest('[hidden]') || target < 2) return;
    el.textContent = '0';
    const co = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return;
      co.disconnect();
      const start = performance.now();
      const step = now => {
        const t = Math.min(1, (now - start) / 1600);
        el.textContent = Math.round(target * (1 - Math.pow(1 - t, 3))).toLocaleString('en-IN');
        if (t < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }, { threshold: 0.5 });
    co.observe(el);
  });

  // Reviews slider (the section stays hidden until real customer quotes are added).
  const reviews = document.querySelector('[data-reviews]');
  if (reviews && !reviews.hidden) {
    const track = reviews.querySelector('.reviews-track');
    const move = dir => {
      const card = track.querySelector('.review');
      const width = card ? card.getBoundingClientRect().width + 22 : track.clientWidth;
      const atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
      if (dir > 0 && atEnd) track.scrollTo({ left: 0 });
      else track.scrollBy({ left: dir * width });
    };
    reviews.querySelectorAll('[data-rv]').forEach(b => b.addEventListener('click', () => move(Number(b.dataset.rv))));
    if (!reduceMotion) {
      let timer = setInterval(() => move(1), 6500);
      const stop = () => { if (timer) { clearInterval(timer); timer = null; } };
      ['pointerenter', 'focusin', 'touchstart'].forEach(ev => reviews.addEventListener(ev, stop, { passive: true }));
    }
  }

  // Location map: the live Google map loads as the visitor scrolls near it. If the page
  // it is shown in blocks embedded maps (some previews, strict browser settings), the
  // drawn pin stays with a short note, and the card's Google Maps links still work.
  const mapFrame = document.querySelector('[data-map]');
  if (mapFrame) {
    const canvas = mapFrame.querySelector('[data-map-canvas]');
    const note = mapFrame.querySelector('[data-map-note]');
    let frame = null;
    const onBlocked = e => {
      const directive = e.effectiveDirective || e.violatedDirective || '';
      if (frame && /frame-src|child-src|default-src/.test(directive) && /google\./.test(String(e.blockedURI))) {
        frame.remove();
        frame = null;
        note.hidden = false;
        document.removeEventListener('securitypolicyviolation', onBlocked);
      }
    };
    const loadMap = () => {
      if (frame) return;
      document.addEventListener('securitypolicyviolation', onBlocked);
      frame = document.createElement('iframe');
      frame.title = 'Map showing SVI Control Panel in Bakrol–Bujrang, Ahmedabad';
      frame.referrerPolicy = 'no-referrer-when-downgrade';
      frame.allowFullscreen = true;
      frame.src = mapFrame.dataset.src;
      canvas.append(frame);
      setTimeout(() => document.removeEventListener('securitypolicyviolation', onBlocked), 15000);
    };
    if ('IntersectionObserver' in window) {
      const near = new IntersectionObserver(([entry]) => { if (entry.isIntersecting) { near.disconnect(); loadMap(); } }, { rootMargin: '600px 0px' });
      near.observe(mapFrame);
    } else {
      loadMap();
    }
  }

  /* ---------- Enquiry form ---------- */
  const form = document.querySelector('#enquiry-form');
  if (!form) return;
  const statusEl = form.querySelector('#form-status');
  const submit = form.querySelector('[data-submit]');
  const emailButton = form.querySelector('[data-send-email]');
  const waButton = form.querySelector('[data-send-whatsapp]');
  const phone = form.elements.phone;
  const WHATSAPP = form.dataset.whatsapp;
  const EMAIL = form.dataset.email;
  const submitLabel = submit.innerHTML;

  let mode = 'checking'; // 'online' | 'offline'
  let busy = true; // true while checking availability or sending
  // Mark the button busy without disabling it, so keyboard focus stays on it.
  const setBusy = on => { busy = on; submit.setAttribute('aria-disabled', String(on)); };
  let widgetId = null;
  let token = null;

  const setStatus = (text, tone = '') => {
    statusEl.textContent = text;
    statusEl.className = 'form-status' + (tone ? ` is-${tone}` : '');
  };

  // Product "Enquire" links pre-select the panel type.
  document.querySelectorAll('[data-product]').forEach(link => link.addEventListener('click', () => {
    const select = form.elements.panel_type;
    if ([...select.options].some(o => o.value === link.dataset.product)) select.value = link.dataset.product;
  }));

  // Phone must contain at least 7 digits (the pattern alone would accept "-------").
  phone.addEventListener('input', () => {
    const v = phone.value.trim();
    const digits = v.replace(/\D/g, '').length;
    const bad = v && (!/^[+()\d\s.-]{7,30}$/.test(v) || digits < 7 || digits > 15);
    phone.setCustomValidity(bad ? 'Please enter a phone number with 7 to 15 digits.' : '');
  });
  form.addEventListener('input', e => { if (e.target.hasAttribute('aria-invalid')) e.target.removeAttribute('aria-invalid'); });

  const validate = () => {
    phone.dispatchEvent(new Event('input'));
    let valid = true;
    [...form.elements].forEach(el => {
      if (!el.willValidate || el.name === 'website') return;
      const ok = el.checkValidity();
      if (!ok) el.setAttribute('aria-invalid', 'true');
      valid = valid && ok;
    });
    if (!valid) form.reportValidity();
    return valid;
  };

  const values = () => {
    const v = Object.fromEntries(new FormData(form));
    v.consent = form.elements.consent.checked;
    return v;
  };

  const composeText = v => [
    'Hello SVI, I have a panel enquiry.',
    '',
    `Name: ${v.name}`,
    v.company ? `Company: ${v.company}` : null,
    `Phone: ${v.phone}`,
    `Email: ${v.email}`,
    v.panel_type ? `Panel type: ${v.panel_type}` : null,
    '',
    v.message
  ].filter(line => line !== null).join('\n');

  const openWhatsApp = () => {
    const url = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(composeText(values()))}`;
    const win = window.open(url, '_blank', 'noopener');
    if (!win) window.location.href = url;
    setStatus('WhatsApp has opened with your message. Press send there to reach us.', 'ok');
  };
  const openEmail = () => {
    const v = values();
    const subject = `Panel enquiry${v.company ? ` from ${v.company}` : ''}`;
    window.location.href = `mailto:${EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(composeText(v))}`;
    setStatus('Your email app has opened with the message. Press send there to reach us.', 'ok');
  };

  // Offline: the main button already sends on WhatsApp, so only email is added.
  // Online: after a failure, both WhatsApp and email are offered as alternatives.
  const showAlternatives = show => {
    emailButton.hidden = !show;
    waButton.hidden = !show || mode !== 'online';
  };

  const goOffline = reason => {
    mode = 'offline';
    setBusy(false);
    submit.innerHTML = 'Send on WhatsApp <span aria-hidden="true">→</span>';
    showAlternatives(true);
    setStatus(reason || 'Your message will open in WhatsApp or your email app, ready to send.');
  };

  const loadTurnstile = siteKey => new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('timeout')), 12000);
    const script = document.createElement('script');
    script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
    script.async = true;
    script.onload = () => {
      clearTimeout(timer);
      if (!window.turnstile) return reject(new Error('missing'));
      widgetId = window.turnstile.render('#security-check', {
        sitekey: siteKey,
        action: 'enquiry',
        theme: 'dark',
        size: 'flexible',
        callback: t => { token = t; if (statusEl.dataset.waiting) { delete statusEl.dataset.waiting; setStatus(''); } },
        'expired-callback': () => { token = null; },
        'error-callback': () => { token = null; setStatus('The security check had a problem. Please try again, or use WhatsApp or email.', 'error'); showAlternatives(true); }
      });
      resolve();
    };
    script.onerror = () => { clearTimeout(timer); reject(new Error('blocked')); };
    document.head.append(script);
  });

  const init = async () => {
    setBusy(true);
    setStatus('');
    try {
      const response = await fetch('/api/form-config', { headers: { Accept: 'application/json' }, signal: AbortSignal.timeout ? AbortSignal.timeout(6000) : undefined });
      const config = response.ok ? await response.json() : { ready: false };
      if (!config.ready || !config.siteKey) return goOffline();
      await loadTurnstile(config.siteKey);
      mode = 'online';
      setBusy(false);
    } catch {
      goOffline();
    }
  };

  const sendOnline = async () => {
    if (!token) {
      statusEl.dataset.waiting = '1';
      setStatus('Please complete the security check above, then press send.', 'error');
      return;
    }
    setBusy(true);
    submit.textContent = 'Sending…';
    setStatus('');
    try {
      const response = await fetch('/api/enquiry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ ...values(), token })
      });
      let result = {};
      try { result = await response.json(); } catch { /* non-JSON error page */ }
      if (!response.ok || !result.ok) {
        const err = new Error(result.error || 'We could not confirm delivery. Please try again, or send it on WhatsApp or email.');
        err.retryable = response.status >= 500 || !result.error;
        throw err;
      }
      form.reset();
      showAlternatives(false);
      setStatus('Thank you. Your enquiry has reached SVI and we will get back to you soon.', 'ok');
    } catch (error) {
      setStatus(error.message || 'We could not confirm delivery. Please try again, or send it on WhatsApp or email.', 'error');
      if (error.retryable !== false) showAlternatives(true);
    } finally {
      token = null;
      if (window.turnstile && widgetId !== null) window.turnstile.reset(widgetId);
      setBusy(false);
      submit.innerHTML = submitLabel;
    }
  };

  form.addEventListener('submit', e => {
    e.preventDefault();
    if (busy || !validate()) return;
    if (mode === 'online') sendOnline();
    else openWhatsApp();
  });

  emailButton.addEventListener('click', () => { if (validate()) openEmail(); });
  waButton.addEventListener('click', () => { if (validate()) openWhatsApp(); });

  init();
})();
