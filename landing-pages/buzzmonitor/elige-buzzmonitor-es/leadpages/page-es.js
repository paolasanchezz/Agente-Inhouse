(function () {
  try { window.jotformEmbedHandler("iframe[id='JotFormIFrame-241825239057661']", "https://form.jotform.com/"); } catch (e) {}

  var root = document.getElementById('bzm');
  if (!root) return;
  var $ = function (s, c) { return (c || root).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || root).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fmt = function (n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); };

  /* ---------- smooth scroll ---------- */
  $$('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var t = document.getElementById(a.getAttribute('href').slice(1));
      if (!t) return;
      e.preventDefault();
      window.scrollTo({ top: t.getBoundingClientRect().top + window.pageYOffset - 76, behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  /* ---------- counters ---------- */
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

  /* ---------- reveal on scroll ---------- */
  var io = new IntersectionObserver(function (ents) {
    ents.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('is-in');
      $$('[data-count]', en.target).forEach(countUp);
      if (en.target.dataset.count) countUp(en.target);
      io.unobserve(en.target);
    });
  }, { threshold: .15, rootMargin: '0px 0px -40px 0px' });
  $$('.bz-rv, .bz-wall, .bz-stats, [data-count]').forEach(function (el) { io.observe(el); });

  /* ---------- nav ---------- */
  var nav = $('.bz-nav'), bar = $('.bz-progress'), links = $$('.bz-nav__links a');
  var device = $('.bz-hero__device');
  var ticking = false;
  function onScroll() {
    var y = window.pageYOffset, h = document.documentElement.scrollHeight - window.innerHeight;
    nav.classList.toggle('is-solid', y > 30);
    bar.style.transform = 'scaleX(' + (h > 0 ? y / h : 0) + ')';
    if (device && !reduce) {
      var r = device.getBoundingClientRect(), p = Math.min(Math.max(1 - (r.top - 80) / (window.innerHeight * .7), 0), 1);
      device.style.transform = 'rotateX(' + (24 - 24 * p).toFixed(2) + 'deg) scale(' + (.9 + .1 * p).toFixed(3) + ')';
    }
    var cur = null;
    links.forEach(function (a) {
      var s = document.getElementById(a.getAttribute('href').slice(1));
      if (s && s.getBoundingClientRect().top < window.innerHeight * .4) cur = a;
    });
    links.forEach(function (a) { a.classList.toggle('is-on', a === cur); });
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* ---------- spotlight ---------- */
  $$('.bz-spot').forEach(function (el) {
    el.addEventListener('pointermove', function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      el.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* ---------- price card tilt ---------- */
  $$('[data-tilt]').forEach(function (el) {
    if (reduce || window.matchMedia('(hover: none)').matches) return;
    el.addEventListener('pointermove', function (e) {
      var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      el.style.transform = 'perspective(900px) rotateY(' + (x * 10) + 'deg) rotateX(' + (-y * 10) + 'deg)';
    });
    el.addEventListener('pointerleave', function () { el.style.transform = ''; });
  });

  /* ---------- hero particles ---------- */
  (function () {
    var cv = $('.bz-hero__net'); if (!cv || reduce) return;
    var ctx = cv.getContext('2d'), pts = [], W, H, dpr = Math.min(window.devicePixelRatio || 1, 2), mouse = { x: -999, y: -999 }, run = true;
    function size() {
      W = cv.offsetWidth; H = cv.offsetHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.min(90, Math.floor(W * H / 16000)); pts = [];
      for (var i = 0; i < n; i++) pts.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .35, vy: (Math.random() - .5) * .35 });
    }
    function draw() {
      if (!run) return;
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i]; p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > W) p.vx *= -1; if (p.y < 0 || p.y > H) p.vy *= -1;
        for (var j = i + 1; j < pts.length; j++) {
          var q = pts[j], dx = p.x - q.x, dy = p.y - q.y, d = dx * dx + dy * dy;
          if (d < 15000) { ctx.strokeStyle = 'rgba(235,124,46,' + (.22 * (1 - d / 15000)) + ')'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke(); }
        }
        var md = (p.x - mouse.x) * (p.x - mouse.x) + (p.y - mouse.y) * (p.y - mouse.y);
        ctx.fillStyle = md < 22000 ? 'rgba(252,189,79,.95)' : 'rgba(255,255,255,.45)';
        ctx.beginPath(); ctx.arc(p.x, p.y, md < 22000 ? 2.2 : 1.4, 0, 6.3); ctx.fill();
        if (md < 22000) { ctx.strokeStyle = 'rgba(252,189,79,' + (.35 * (1 - md / 22000)) + ')'; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke(); }
      }
      requestAnimationFrame(draw);
    }
    var hero = $('.bz-hero');
    hero.addEventListener('pointermove', function (e) { var r = cv.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    hero.addEventListener('pointerleave', function () { mouse.x = mouse.y = -999; });
    new IntersectionObserver(function (e) { var v = e[0].isIntersecting; if (v && !run) { run = true; draw(); } run = v; }).observe(hero);
    window.addEventListener('resize', size);
    size(); draw();
  })();

  /* ---------- comparison ---------- */
  (function () {
    var arena = $('.bz-arena'); if (!arena) return;
    var tabs = $$('.bz-tab', arena), pill = $('.bz-tabs__pill', arena), rows = $$('.bz-row', arena);
    var nameEl = $('#bz-cp-name'), scoreEl = $('#bz-cp-score');
    var names = tabs.map(function (t) { return t.textContent.trim(); });
    var data = rows.map(function (r) { return r.dataset.states.split(',').map(Number); });
    var total = rows.length;
    var scores = names.map(function (_, i) { return data.reduce(function (s, r) { return s + r[i]; }, 0); });
    var C = 2 * Math.PI * 44;
    var ICON_Y = '<svg viewBox="0 0 24 24"><path d="M5 12l5 5L20 7"/></svg>', ICON_N = '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>';
    var ringBm = $('.bz-ring--bm .fg', arena), ringCp = $('.bz-ring--cp .fg', arena);
    [ringBm, ringCp].forEach(function (c) { c.style.strokeDasharray = C; c.style.strokeDashoffset = C; });

    rows.forEach(function (r) {
      var c = r.querySelectorAll('.bz-row__c');
      c[0].innerHTML = '<span class="bz-mark bz-mark--y" aria-label="Buzzmonitor: sí">' + ICON_Y + '</span>';
    });

    var cur = 0, timer = null, DUR = 4500, visible = false, hovering = false, mode = 'duel';

    function movePill() {
      var t = tabs[cur];
      pill.style.width = t.offsetWidth + 'px';
      pill.style.transform = 'translateX(' + (t.offsetLeft - 4) + 'px)';
    }
    function animScore(to) {
      var from = +scoreEl.textContent, t0 = null;
      function st(t) { if (!t0) t0 = t; var p = Math.min((t - t0) / 700, 1); scoreEl.textContent = Math.round(from + (to - from) * p); if (p < 1) requestAnimationFrame(st); }
      requestAnimationFrame(st);
    }
    function render(i) {
      cur = i;
      tabs.forEach(function (t, k) { t.classList.toggle('is-on', k === i); t.classList.remove('is-run'); t.setAttribute('aria-selected', k === i); });
      movePill();
      nameEl.textContent = names[i];
      nameEl.classList.remove('is-swap'); void nameEl.offsetWidth; nameEl.classList.add('is-swap');
      rows.forEach(function (r, k) {
        var ok = data[k][i] === 1, cell = r.querySelectorAll('.bz-row__c')[1];
        cell.innerHTML = '<span class="bz-mark ' + (ok ? 'bz-mark--cy' : 'bz-mark--n') + ' is-flip" style="--fd:' + (k * 55) + 'ms" aria-label="' + names[i] + ': ' + (ok ? 'sí' : 'no') + '">' + (ok ? ICON_Y : ICON_N) + '</span>';
        r.classList.toggle('is-win', !ok);
      });
      ringBm.style.strokeDashoffset = 0;
      ringCp.style.strokeDashoffset = C * (1 - scores[i] / total);
      animScore(scores[i]);
      schedule();
    }
    function schedule() {
      clearTimeout(timer);
      tabs.forEach(function (t) { t.classList.remove('is-run'); });
      if (reduce || !visible || hovering || mode !== 'duel') return;
      var t = tabs[cur]; t.style.setProperty('--t', DUR + 'ms'); void t.offsetWidth; t.classList.add('is-run');
      timer = setTimeout(function () { render((cur + 1) % tabs.length); }, DUR);
    }
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () {
        if (mode !== 'duel') setMode('duel');
        render(k);
        t.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
      });
    });
    arena.addEventListener('mouseenter', function () { hovering = true; schedule(); });
    arena.addEventListener('mouseleave', function () { hovering = false; schedule(); });
    window.addEventListener('resize', movePill);

    /* full matrix */
    var mx = $('.bz-matrix', arena), html = '<table><thead><tr><th scope="col">Funcionalidad</th><th scope="col" class="is-bm"><img src="' + $('.bz-score__name img', arena).getAttribute('src') + '" alt="Buzzmonitor"></th>';
    names.forEach(function (n) { html += '<th scope="col">' + n + '</th>'; });
    html += '</tr></thead><tbody>';
    rows.forEach(function (r, k) {
      html += '<tr><td>' + r.querySelector('.bz-row__f').innerHTML + '</td><td class="is-bm"><span class="bz-dot bz-dot--bm" style="--dd:' + (k * 40) + 'ms"></span></td>';
      data[k].forEach(function (v, c) { html += '<td><span class="bz-dot ' + (v ? 'bz-dot--y' : 'bz-dot--n') + '" style="--dd:' + (k * 40 + (c + 1) * 30) + 'ms"></span></td>'; });
      html += '</tr>';
    });
    html += '</tbody><tfoot><tr><td></td><td class="is-bm">' + total + '<small>/' + total + '</small></td>';
    scores.forEach(function (s) { html += '<td>' + s + '<small>/' + total + '</small></td>'; });
    html += '</tr></tfoot></table>';
    mx.innerHTML = html;
    var cells = $$('th, td', mx);
    $$('tr', mx).forEach(function (tr) {
      Array.prototype.forEach.call(tr.children, function (td, ci) {
        if (ci < 2) return;
        td.addEventListener('mouseenter', function () { $$('tr', mx).forEach(function (r) { r.children[ci] && r.children[ci].classList.add('col-hover'); }); });
        td.addEventListener('mouseleave', function () { cells.forEach(function (c) { c.classList.remove('col-hover'); }); });
      });
    });

    var modeBtns = $$('.bz-mode button', arena);
    function setMode(m) {
      mode = m;
      modeBtns.forEach(function (b) { b.classList.toggle('is-on', b.dataset.mode === m); });
      arena.classList.toggle('is-all', m === 'all');
      arena.classList.remove('is-drawn');
      if (m === 'all') { void arena.offsetWidth; requestAnimationFrame(function () { arena.classList.add('is-drawn'); }); }
      schedule();
    }
    modeBtns.forEach(function (b) { b.addEventListener('click', function () { setMode(b.dataset.mode); }); });

    new IntersectionObserver(function (e) {
      var was = visible; visible = e[0].isIntersecting;
      if (visible && !was) render(cur); else schedule();
    }, { threshold: .3 }).observe(arena);
    setTimeout(movePill, 300);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(movePill);
  })();

  /* ---------- features explorer ---------- */
  (function () {
    var btns = $$('.bz-ex__btn'), panels = $$('.bz-panel');
    panels.forEach(function (p) { $$('li', p).forEach(function (li, i) { li.style.setProperty('--i', i); }); });
    btns.forEach(function (b, k) {
      b.setAttribute('aria-selected', k === 0);
      b.addEventListener('click', function () {
        btns.forEach(function (x, j) { x.classList.toggle('is-on', j === k); x.setAttribute('aria-selected', j === k); });
        panels.forEach(function (p, j) { p.classList.toggle('is-on', j === k); });
        if (window.innerWidth < 960) b.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
      });
    });
  })();
})();
