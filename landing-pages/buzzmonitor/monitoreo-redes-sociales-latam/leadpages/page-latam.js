
(function(){
  /* ---- scroll reveal ---- */
  var items = document.querySelectorAll('.reveal');
  function showAll(){ Array.prototype.forEach.call(items, function(el){ el.classList.add('is-visible'); }); }
  if(!('IntersectionObserver' in window)){
    showAll();
  } else {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold:0.12, rootMargin:'0px 0px -60px 0px' });
    Array.prototype.forEach.call(items, function(el){ io.observe(el); });
  }

  /* ---- o video vive dentro de um wrapper que comeca em opacity:0;
         alguns browsers pausam o autoplay nesse estado ---- */
  var v = document.getElementById('hero-video');
  if(v){
    var kick = function(){ var p = v.play(); if(p && p.catch){ p.catch(function(){}); } };
    kick();
    window.addEventListener('load', kick, { once:true });
  }

  /* ---- popover dos chips: nunca sair da viewport ---- */
  function place(net){
    var pop = net.querySelector('.net__pop');
    if(!pop) return;
    pop.style.left = '50%';
    pop.style.setProperty('--arrow-x', '50%');
    var r = pop.getBoundingClientRect();
    var pad = 10, shift = 0;
    if(r.left < pad) shift = pad - r.left;
    else if(r.right > window.innerWidth - pad) shift = (window.innerWidth - pad) - r.right;
    if(shift){
      pop.style.left = 'calc(50% + ' + Math.round(shift) + 'px)';
      pop.style.setProperty('--arrow-x', 'calc(50% - ' + Math.round(shift) + 'px)');
    }
  }
  var nets = document.querySelectorAll('.net');
  function placeAll(){ Array.prototype.forEach.call(nets, place); }

  /* ---- o popover abre e FICA aberto: so fecha no X, no Esc, num clique fora
         ou ao abrir outro chip. O hover tambem abre; ao sair do grupo espera
         600ms, tempo de o ponteiro atravessar o vao e chegar no CTA ---- */
  var openNet = null, closeTimer = null;
  function closeNet(){
    if(closeTimer){ clearTimeout(closeTimer); closeTimer = null; }
    if(openNet){ openNet.classList.remove('is-open'); openNet = null; }
  }
  function openNetFor(net){
    if(closeTimer){ clearTimeout(closeTimer); closeTimer = null; }
    if(openNet && openNet !== net) openNet.classList.remove('is-open');
    openNet = net;
    net.classList.add('is-open');
    place(net);
  }
  function scheduleClose(){
    if(closeTimer) clearTimeout(closeTimer);
    closeTimer = setTimeout(closeNet, 600);
  }
  Array.prototype.forEach.call(nets, function(net){
    var pop = net.querySelector('.net__pop');
    if(pop && !pop.querySelector('.net__close')){
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'net__close';
      btn.setAttribute('aria-label', 'Cerrar');
      btn.innerHTML = '&times;';
      btn.addEventListener('click', function(e){ e.stopPropagation(); closeNet(); });
      pop.appendChild(btn);
      var cta = pop.querySelector('.net__cta');
      if(cta) cta.addEventListener('click', function(){ setTimeout(closeNet, 60); });
    }
    net.addEventListener('mouseenter', function(){ openNetFor(net); });
    net.addEventListener('mouseleave', scheduleClose);
    net.addEventListener('focusin', function(){ openNetFor(net); });
    net.addEventListener('focusout', function(e){
      if(!net.contains(e.relatedTarget)) scheduleClose();
    });
    net.addEventListener('click', function(){ openNetFor(net); });
    net.addEventListener('touchstart', function(){ openNetFor(net); }, { passive:true });
    net.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); openNetFor(net); }
    });
  });
  document.addEventListener('click', function(e){
    if(openNet && !openNet.contains(e.target)) closeNet();
  });
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' || e.key === 'Esc') closeNet();
  });
  /* posiciona tudo de saida (e a cada resize) pra que nem o popover escondido
     estoure a viewport e crie scroll horizontal */
  placeAll();
  window.addEventListener('load', placeAll, { once:true });
  var t; window.addEventListener('resize', function(){ clearTimeout(t); t = setTimeout(placeAll, 120); });
})();

(function(){
  var f=document.getElementById('videoFacade');
  if(!f)return;
  f.addEventListener('click',function(){
    var ifr=document.createElement('iframe');
    ifr.src='https://www.youtube.com/embed/nBMZZZKrMpI?autoplay=1&rel=0';
    ifr.title='Demostración de la plataforma Buzzmonitor';
    ifr.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    ifr.setAttribute('allowfullscreen','');
    f.replaceWith(ifr);
  });
})();
