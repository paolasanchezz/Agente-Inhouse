(function () {
  var root = document.getElementById('bzl');
  if (!root) return;
  root.classList.add('bz-js');
  var $ = function (s, c) { return (c || root).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || root).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mobile = window.matchMedia('(max-width: 960px)');
  var fmt = function (n) { return Math.round(n).toLocaleString('es-MX'); };
  (function () {
    var params = new URLSearchParams(window.location.search);
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'adposition'].forEach(function (key) {
      var v = params.get(key), el = document.getElementById(key);
      if (v && el) el.value = v;
    });
    var urlField = document.getElementById('page_url');
    if (urlField) urlField.value = window.location.href;
    try {
      var c = { utm_source: params.get('utm_source'), utm_medium: params.get('utm_medium'), utm_campaign: params.get('utm_campaign'), utm_content: params.get('utm_content'), utm_term: params.get('utm_term') };
      var saved = localStorage.getItem('utm_campaign');
      if (!saved || (c.utm_campaign && c.utm_campaign.toLowerCase() !== '[search][institucional][brasil]')) {
        Object.keys(c).forEach(function (k) { localStorage.setItem(k, c[k]); });
      }
    } catch (e) {}
  })();
  var tel = document.getElementById('telefone');
  if (tel) tel.addEventListener('input', function () {
    var d = tel.value.replace(/\D/g, '').slice(0, 11), o = d;
    if (d.length > 10) o = '(' + d.slice(0, 2) + ') ' + d.slice(2, 7) + '-' + d.slice(7);
    else if (d.length > 6) o = '(' + d.slice(0, 2) + ') ' + d.slice(2, 6) + '-' + d.slice(6);
    else if (d.length > 2) o = '(' + d.slice(0, 2) + ') ' + d.slice(2);
    else if (d.length) o = '(' + d;
    tel.value = o;
  });
  var form = $('form');
  if (form) form.addEventListener('submit', function () {
    var b = $('button[type=submit]', form); if (b) b.setAttribute('disabled', '');
  });
  $$('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href').slice(1), t = document.getElementById(id);
      if (!t) return;
      e.preventDefault();
      window.scrollTo({ top: t.getBoundingClientRect().top + window.pageYOffset - 90, behavior: reduce ? 'auto' : 'smooth' });
      if (id === 'form' && !mobile.matches) setTimeout(function () { var f = $('input[type=text]', t); if (f) f.focus({ preventScroll: true }); }, 700);
    });
  });
  function countUp(el) {
    if (el.dataset.done) return; el.dataset.done = 1;
    var to = +el.dataset.count, suf = el.dataset.suffix || '', t0 = null, dur = 1600;
    if (reduce) return;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 4);
      el.textContent = fmt(to * e) + suf;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var io = new IntersectionObserver(function (ents) {
    ents.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('is-in');
      $$('[data-count]', en.target).forEach(countUp);
      if (en.target.dataset.count) countUp(en.target);
      io.unobserve(en.target);
    });
  }, { threshold: .15, rootMargin: '0px 0px -40px 0px' });
  $$('.bl-rv, .bl-wall, [data-count]').forEach(function (el) { io.observe(el); });
  var nav = $('.bl-nav'), bar = $('.bl-progress'), device = $('.bl-hero__device'), ticking = false;
  function onScroll() {
    var y = window.pageYOffset, vh = window.innerHeight, h = document.documentElement.scrollHeight - vh;
    nav.classList.toggle('is-solid', y > 30);
    bar.style.transform = 'scaleX(' + (h > 0 ? y / h : 0) + ')';
    if (device && !reduce) {
      var r = device.getBoundingClientRect(), p = Math.min(Math.max(1 - (r.top - 80) / (vh * .7), 0), 1);
      device.style.transform = 'rotateX(' + (20 - 20 * p).toFixed(2) + 'deg) scale(' + (.92 + .08 * p).toFixed(3) + ')';
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
  (function () {
    var cv = $('.bl-hero__net'); if (!cv || reduce) return;
    var ctx = cv.getContext('2d'), pts = [], W, H, dpr = Math.min(window.devicePixelRatio || 1, 2), mouse = { x: -999, y: -999 }, run = true, lastW = 0;
    function size() {
      W = cv.offsetWidth; H = cv.offsetHeight;
      if (W === lastW && pts.length) return; lastW = W;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.min(W < 700 ? 36 : 84, Math.floor(W * H / 16000)); pts = [];
      for (var i = 0; i < n; i++) pts.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .35, vy: (Math.random() - .5) * .35, c: Math.random() < .5 ? '235,124,46' : '232,64,122' });
    }
    function draw() {
      if (!run) return;
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i]; p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > W) p.vx *= -1; if (p.y < 0 || p.y > H) p.vy *= -1;
        for (var j = i + 1; j < pts.length; j++) {
          var q = pts[j], dx = p.x - q.x, dy = p.y - q.y, d = dx * dx + dy * dy;
          if (d < 15000) { ctx.strokeStyle = 'rgba(' + p.c + ',' + (.2 * (1 - d / 15000)) + ')'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke(); }
        }
        var md = (p.x - mouse.x) * (p.x - mouse.x) + (p.y - mouse.y) * (p.y - mouse.y);
        ctx.fillStyle = 'rgba(' + p.c + ',' + (md < 22000 ? .95 : .5) + ')';
        ctx.beginPath(); ctx.arc(p.x, p.y, md < 22000 ? 2.4 : 1.6, 0, 6.3); ctx.fill();
        if (md < 22000) { ctx.strokeStyle = 'rgba(232,64,122,' + (.3 * (1 - md / 22000)) + ')'; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke(); }
      }
      requestAnimationFrame(draw);
    }
    var hero = $('.bl-hero');
    hero.addEventListener('pointermove', function (e) { var r = cv.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    hero.addEventListener('pointerleave', function () { mouse.x = mouse.y = -999; });
    new IntersectionObserver(function (e) { var v = e[0].isIntersecting; if (v && !run) { run = true; draw(); } run = v; }).observe(hero);
    window.addEventListener('resize', size);
    size(); draw();
  })();
  (function () {
    var imgs = $$('.bl-feat__in img'), thumbs = $('.bl-thumbs'), dotsBox = $('.bl-tdots'), barEl = $('.bl-feat__bar'), feat = $('.bl-feat');
    if (!imgs.length) return;
    var cur = 0, timer = null, DUR = 5500, visible = false, hovering = false, n = imgs.length;
    var dots = imgs.map(function (_, i) {
      var b = document.createElement('button'); b.type = 'button'; b.setAttribute('aria-label', 'Testimonio ' + (i + 1));
      b.addEventListener('click', function () { show(i); }); dotsBox.appendChild(b); return b;
    });
    function show(i) {
      cur = (i + n) % n;
      imgs.forEach(function (im, k) { im.classList.toggle('is-on', k === cur); if (k === cur) im.loading = 'eager'; });
      dots.forEach(function (d, k) { d.classList.toggle('is-on', k === cur); });
      var h = '';
      for (var s = 1; s <= 3; s++) {
        var k = (cur + s) % n;
        h += '<button type="button" class="bl-thumb is-swap" data-k="' + k + '" style="animation-delay:' + (s * 70) + 'ms" aria-label="Ver testimonio ' + (k + 1) + '"><img src="' + imgs[k].getAttribute('src') + '" alt="" loading="lazy" width="640" height="640"></button>';
      }
      thumbs.innerHTML = h;
      $$('.bl-thumb', thumbs).forEach(function (t) { t.addEventListener('click', function () { show(+t.dataset.k); }); });
      schedule();
    }
    function schedule() {
      clearTimeout(timer); barEl.classList.remove('is-run');
      if (reduce || !visible || hovering) return;
      barEl.style.setProperty('--t', DUR + 'ms'); void barEl.offsetWidth; barEl.classList.add('is-run');
      timer = setTimeout(function () { show(cur + 1); }, DUR);
    }
    var sec = $('.bl-testi');
    sec.addEventListener('mouseenter', function () { hovering = true; schedule(); });
    sec.addEventListener('mouseleave', function () { hovering = false; schedule(); });
    var x0 = null;
    feat.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    feat.addEventListener('touchend', function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1)); x0 = null; });
    new IntersectionObserver(function (e) { visible = e[0].isIntersecting; schedule(); }, { threshold: .3 }).observe(sec);
    show(0);
  })();
})();
