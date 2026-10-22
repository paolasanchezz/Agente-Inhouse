(function(){
  /* Reveal on scroll */
  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    for (var i=0;i<els.length;i++) els[i].classList.add('is-in');
  } else {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting){ e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.15 });
    els.forEach(function(el){ io.observe(el); });
  }

  /* Formulario sob demanda (o Jotform pesa ~870 KB). Entra 600 px antes da
     secao, ou antes disso no hover/toque de qualquer CTA que aponte pra ela. */
  var jotHost = document.getElementById('jotHost');
  if (jotHost) {
    var carregaJot = function(){
      if (jotHost.dataset.carregado) return;
      jotHost.dataset.carregado = '1';
      /* Na Leadpages o Jotform vem do form-cxpress-v3.js (source hospedado,
         iframe srcdoc), igual as LPs irmas. Sem ele, cai na contingencia. */
      if (window.cxMountForm) { window.cxMountForm(jotHost); } else { contingencia(); }
      setTimeout(function(){ if (!jotHost.querySelector('iframe')) contingencia(); }, 6000);
    };
    /* Rede de seguranca: se o jsform nao executar (bloqueador, rede), cai para
       iframe simples e, junto, um link para abrir o formulario em nova aba. */
    var contingencia = function(){
      if (jotHost.querySelector('iframe')) return;
      var ns = jotHost.querySelector('noscript');
      if (ns && ns.textContent.indexOf('<iframe') > -1) {
        jotHost.insertAdjacentHTML('beforeend', ns.textContent);
      } else {
        var f = document.createElement('iframe');
        f.src = 'https://form.jotform.com/' + jotHost.dataset.jotform;
        f.title = 'Formulário de contato';
        f.style.cssText = 'width:100%;height:900px;border:0;display:block';
        jotHost.appendChild(f);
      }
      ultimoRecurso();
    };
    var ultimoRecurso = function(){
      if (jotHost.dataset.recurso) return;
      jotHost.dataset.recurso = '1';
      var url = 'https://form.jotform.com/' + jotHost.dataset.jotform;
      jotHost.insertAdjacentHTML('beforeend',
        '<p style="margin:0;background:#fff;border-radius:14px;padding:20px;text-align:center;font-size:16px">' +
        '<a href="' + url + '" target="_blank" rel="noopener" style="color:#232960;font-weight:700">Abrir o formulário em uma nova aba</a></p>');
    };
    var sec = jotHost.closest ? jotHost.closest('section[id]') : null;
    if (sec && sec.id) {
      var atalhos = document.querySelectorAll('a[href="#' + sec.id + '"]');
      Array.prototype.forEach.call(atalhos, function(a){
        ['pointerenter', 'touchstart', 'click'].forEach(function(ev){
          a.addEventListener(ev, carregaJot, {once: true, passive: true});
        });
      });
    }
    if ('IntersectionObserver' in window && sec) {
      var ioJot = new IntersectionObserver(function(en){
        en.forEach(function(e){ if (e.isIntersecting){ ioJot.disconnect(); carregaJot(); } });
      }, {rootMargin: '600px 0px'});
      ioJot.observe(sec);
    } else {
      carregaJot();
    }
  }

  /* Cenas animadas: pausam quando o bloco sai de vista. */
  var fx = document.querySelectorAll('[data-fx]');
  if (fx.length && 'IntersectionObserver' in window) {
    var ioFx = new IntersectionObserver(function(entradas){
      entradas.forEach(function(e){ e.target.classList.toggle('fx-idle', !e.isIntersecting); });
    }, {threshold:.08});
    fx.forEach(function(el){ el.classList.add('fx-idle'); ioFx.observe(el); });
  }

  /* Contagem dos numeros da cena. O valor final JA esta no HTML: sem JS ou com
     movimento reduzido, o numero fica certo e nunca travado no zero. */
  var nums = document.querySelectorAll('[data-count-to]');
  if (nums.length && 'IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var ioNum = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (!e.isIntersecting) return;
        ioNum.unobserve(e.target);
        var el = e.target, alvo = parseFloat(el.getAttribute('data-count-to')), t0 = null;
        el.textContent = '0';
        (function frame(ts){
          if (t0 === null) t0 = ts;
          var p = Math.min((ts - t0) / 1800, 1);
          el.textContent = Math.round(alvo * (1 - Math.pow(1 - p, 3))).toLocaleString('pt-BR');
          if (p < 1) requestAnimationFrame(frame);
        })(performance.now());
      });
    }, {threshold:.4});
    nums.forEach(function(el){ ioNum.observe(el); });
  }

  /* Holofote do hero: so escreve --mx/--my. Sem rAF, sem loop. */
  var hero = document.querySelector('.hero'), dots = document.getElementById('heroDots');
  if (hero && dots && matchMedia('(pointer: fine)').matches &&
      !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    hero.addEventListener('pointermove', function(e){
      var r = hero.getBoundingClientRect();
      dots.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      dots.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }, {passive:true});
  }
})();
