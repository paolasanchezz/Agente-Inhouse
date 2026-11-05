(function(){
  var root=document.querySelector('.bzia'); if(!root || window.__bziaInit) return; window.__bziaInit=true;
  /* o editor do Leadpages salva o HTML ja modificado pelo script: limpa esses restos antes de iniciar */
  root.removeAttribute('data-bzia-init');
  Array.prototype.forEach.call(root.querySelectorAll('.is-lit'),function(el){el.classList.remove('is-lit');});
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var navH=function(){return (root.querySelector('.nav')||{}).offsetHeight||64;};

  /* Tami: video WebM com transparencia (fluido); Safari recebe o WebP animado. Comeca quando a hero aparece */
  (function(){ var t=root.querySelector('.tami'); if(!t || getComputedStyle(t).display==='none') return;
    var v=t.querySelector('.tami__vid'), im=t.querySelector('.tami__img'), an=t.querySelector('.tami__anim');
    if(reduce){ t.classList.add('is-img'); return; }
    var ua=navigator.userAgent, isSafari=/^((?!chrome|chromium|android|crios|fxios|edg).)*safari/i.test(ua);
    var webmOk=!isSafari && v && v.canPlayType && v.canPlayType('video/webm; codecs="vp9"');
    var started=false;
    function useImg(){ if(v){ try{v.pause();}catch(e){} } var a=new Image(); a.onload=function(){ im.src=a.src; t.classList.remove('is-vid'); t.classList.add('is-img'); }; a.onerror=function(){ t.classList.add('is-img'); }; a.src=an.currentSrc||an.src; }
    function go(){ if(started || document.hidden) return; started=true;
      if(webmOk){ v.addEventListener('playing',function(){ t.classList.add('is-vid'); },{once:true}); v.addEventListener('error',useImg,{once:true});
        try{ v.currentTime=0; }catch(e){} var pr=v.play(); if(pr && pr.catch) pr.catch(useImg); }
      else useImg(); }
    if('IntersectionObserver' in window) new IntersectionObserver(function(e){ if(e[0].isIntersecting) setTimeout(go,600); },{threshold:.3}).observe(t.parentNode);
    else go();
    document.addEventListener('visibilitychange',function(){ if(!document.hidden) go(); }); })();

  /* Rede de linhas no hero (decorativa) */
  (function(){ var cv=root.querySelector('.hero__net'); if(!cv || reduce) return; var ctx=cv.getContext('2d'), pts=[], W, H, dpr=Math.min(window.devicePixelRatio||1,2), run=true, hero=root.querySelector('.hero');
    function size(){ W=cv.offsetWidth; H=cv.offsetHeight; cv.width=W*dpr; cv.height=H*dpr; ctx.setTransform(dpr,0,0,dpr,0,0); var n=Math.min(60,Math.floor(W*H/22000)); pts=[]; for(var i=0;i<n;i++) pts.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.25,vy:(Math.random()-.5)*.25}); }
    function draw(){ if(!run) return; ctx.clearRect(0,0,W,H);
      for(var i=0;i<pts.length;i++){ var p=pts[i]; p.x+=p.vx; p.y+=p.vy; if(p.x<0||p.x>W) p.vx*=-1; if(p.y<0||p.y>H) p.vy*=-1;
        for(var j=i+1;j<pts.length;j++){ var q=pts[j], dx=p.x-q.x, dy=p.y-q.y, d=dx*dx+dy*dy; if(d<16000){ ctx.strokeStyle='rgba(235,124,46,'+(.18*(1-d/16000))+')'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(q.x,q.y); ctx.stroke(); } }
        ctx.fillStyle='rgba(247,178,27,.5)'; ctx.beginPath(); ctx.arc(p.x,p.y,1.6,0,6.3); ctx.fill(); }
      requestAnimationFrame(draw); }
    if('IntersectionObserver' in window) new IntersectionObserver(function(e){ var v=e[0].isIntersecting; if(v && !run){ run=true; draw(); } run=v; }).observe(hero);
    window.addEventListener('resize',size); size(); draw(); })();

  /* Scroll suave com compensacao do menu fixo */
  function goTo(id){
    var t=document.getElementById(id); if(!t) return false;
    var extra=t.hasAttribute('data-spy-target')&&t.classList.contains('mod')?70:12;
    window.scrollTo({top:t.getBoundingClientRect().top+window.pageYOffset-navH()-extra,behavior:reduce?'auto':'smooth'});
    return true;
  }
  root.querySelectorAll('a[href^="#bzia-"]:not([data-netd-cta])').forEach(function(a){
    a.addEventListener('click',function(e){ if(goTo(a.getAttribute('href').slice(1))) e.preventDefault(); });
  });

  /* Reveal */
  var els=root.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('visible');ro.unobserve(e.target);}});},{threshold:.12});
    els.forEach(function(el){ro.observe(el);});
  } else els.forEach(function(el){el.classList.add('visible');});

  /* Contadores */
  function fmt(n){return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g,'.');}
  var counters=root.querySelectorAll('[data-count]');
  if('IntersectionObserver' in window && !reduce){
    var co=new IntersectionObserver(function(es){es.forEach(function(e){
      if(!e.isIntersecting) return; co.unobserve(e.target);
      var el=e.target,end=+el.getAttribute('data-count'),suf=el.getAttribute('data-suffix')||'',t0=null,dur=1400;
      (function step(ts){ if(!t0) t0=ts; var p=Math.min((ts-t0)/dur,1),v=Math.round(end*(1-Math.pow(1-p,3))); el.textContent=fmt(v)+suf; if(p<1) requestAnimationFrame(step); })(performance.now());
    });},{threshold:.6});
    counters.forEach(function(c){co.observe(c);});
  }

  /* Menu: sombra ao rolar + scrollspy nos modulos */
  var nav=root.querySelector('.nav'), links=root.querySelectorAll('[data-spy]'), targets=root.querySelectorAll('[data-spy-target]');
  var mcta=document.getElementById('bzia-mcta'), form=document.getElementById('bzia-form'), hero=root.querySelector('.hero');
  var ticking=false;
  function onScroll(){
    ticking=false;
    var y=window.pageYOffset; nav&&nav.classList.toggle('is-scrolled',y>8);
    var line=navH()+140, cur=null;
    targets.forEach(function(t){ var r=t.getBoundingClientRect(); if(r.top<=line && r.bottom>line) cur=t.id; });
    links.forEach(function(l){ l.classList.toggle('is-active',l.getAttribute('data-spy')===cur); });
    if(mcta&&hero&&form){
      var hb=hero.getBoundingClientRect().bottom, fr=form.getBoundingClientRect(), fvis=fr.top<window.innerHeight&&fr.bottom>0;
      mcta.classList.toggle('is-on',hb<0&&!fvis);
    }
  }
  window.addEventListener('scroll',function(){ if(!ticking){ ticking=true; requestAnimationFrame(onScroll);} },{passive:true});
  onScroll();

  /* Canais: destaque passeando pelos icones (para ao interagir) */
  var chans=root.querySelectorAll('.chan__it'), litTimer=null;
  if(chans.length && !reduce){
    var li=0; litTimer=setInterval(function(){ chans.forEach(function(c){c.classList.remove('is-lit');}); chans[li%chans.length].classList.add('is-lit'); li+=5; if(li%chans.length===0) li++; },1100);
  }
  function stopLit(){ if(litTimer){ clearInterval(litTimer); litTimer=null; chans.forEach(function(c){c.classList.remove('is-lit');}); } }

  /* Modal das redes (conteudo em #bzia-redes, gerado de redes.json) */
  /* icones das redes vem do asset redes-es.js (tirados do HTML para caber na API) */
  var IC=window.__BZIA_IC||{};
  Array.prototype.forEach.call(root.querySelectorAll('.chan__it'),function(b){ var im=b.querySelector('img'); if(im && !im.getAttribute('src') && IC[b.getAttribute('data-net')]) im.src=IC[b.getAttribute('data-net')]; });
  var dlg=document.getElementById('bzia-netd');
  if(window.__BZIA_REDES && dlg){
    var NETS=window.__BZIA_REDES, order=Object.keys(NETS), cur=0, lastBtn=null;
    var SCOPE={pub:'Perfiles y términos públicos',adm:'Cuentas de tu marca'};
    var ICO_PUB='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>';
    var ICO_ADM='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>';
    var byId=function(id){return document.getElementById(id);};
    function chip(txt,ico){ var c=document.createElement('span'); c.className='netd__chip'; c.innerHTML=ico; c.appendChild(document.createTextNode(txt)); return c; }
    function fill(i){
      cur=(i+order.length)%order.length; var n=NETS[order[cur]];
      var bi=root.querySelector('.chan__it[data-net="'+order[cur]+'"] img'); if(bi) byId('bzia-netd-ic').src=bi.src; byId('bzia-netd-t').textContent=n.nome; byId('bzia-netd-lead').textContent=n.lead; byId('bzia-netd-time').textContent=n.tempo;
      var sc=byId('bzia-netd-scope'); sc.innerHTML='';
      if(n.escopo!=='adm') sc.appendChild(chip(SCOPE.pub,ICO_PUB));
      if(n.escopo!=='pub') sc.appendChild(chip(SCOPE.adm,ICO_ADM));
      var ls=byId('bzia-netd-list'); ls.innerHTML='';
      n.itens.forEach(function(it){ var r=document.createElement('div'); r.className='netd__row'; var l=document.createElement('span'); l.className='netd__lbl'; l.textContent=it[0]; var t=document.createElement('span'); t.textContent=it[1]; r.appendChild(l); r.appendChild(t); ls.appendChild(r); });
      var bd=dlg.querySelector('.netd__body'); if(bd) bd.scrollTop=0;
      if(window.dataLayer) window.dataLayer.push({event:'bzia_rede_aberta',rede:order[cur]});
    }
    function openNet(id,btn){
      stopLit(); lastBtn=btn||null; fill(Math.max(0,order.indexOf(id)));
      if(typeof dlg.showModal==='function'){ if(!dlg.open) dlg.showModal(); } else dlg.setAttribute('open','');
      document.documentElement.style.overflow='hidden';
    }
    function closeNet(){ document.documentElement.style.overflow=''; if(typeof dlg.close==='function'){ if(dlg.open) dlg.close(); } else dlg.removeAttribute('open'); }
    dlg.addEventListener('close',function(){ document.documentElement.style.overflow=''; if(lastBtn) lastBtn.focus({preventScroll:true}); });
    chans.forEach(function(c){ c.addEventListener('click',function(){ openNet(c.getAttribute('data-net'),c); }); });
    dlg.addEventListener('click',function(e){
      if(e.target===dlg || e.target.closest('[data-netd-close]')) return closeNet();
      var st=e.target.closest('[data-netd-step]'); if(st) return fill(cur+Number(st.getAttribute('data-netd-step')));
      if(e.target.closest('[data-netd-cta]')){ e.preventDefault(); lastBtn=null; closeNet(); goTo('bzia-form'); }
    });
    dlg.addEventListener('keydown',function(e){ if(e.key==='ArrowRight') fill(cur+1); if(e.key==='ArrowLeft') fill(cur-1); });
  }

  /* Video: carrega o YouTube so no clique */
  var vid=document.getElementById('bzia-video');
  if(vid){ var btn=vid.querySelector('.vid__poster'); btn&&btn.addEventListener('click',function(){
    var f=document.createElement('iframe');
    f.src='https://www.youtube.com/embed/'+vid.getAttribute('data-yt')+'?autoplay=1&rel=0&playsinline=1';
    f.title='La inteligencia artificial y Buzzmonitor lo cambian todo';
    f.setAttribute('allow','accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'); f.setAttribute('allowfullscreen','');
    vid.innerHTML=''; vid.appendChild(f);
  }); }

})();
