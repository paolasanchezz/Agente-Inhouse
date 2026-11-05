(function(){
  var q=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
  var root=q('#bzm')[0];if(!root)return;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  // O editor da Leadpages roda estes scripts (blob:) e grava no HTML o que eles injetam. Nele, nada e injetado.
  var editor=/^(blob|about):/.test(location.protocol)||(location.ancestorOrigins&&location.ancestorOrigins.length>0&&/(^|\.)leadpages\.com$/.test((location.ancestorOrigins[0]||'').replace(/^https?:\/\//,'')));
  q('.bz-mctl',root).forEach(function(el){el.parentNode.removeChild(el)});
  q('.bz-hub__track',root).forEach(function(el){el.parentNode.removeChild(el)});
  root.classList.remove('is-paused');
  if(editor){root.classList.remove('js');root.classList.add('is-editor');return}
  root.classList.remove('is-editor');
  root.classList.add('js');

  var fmt=function(n){return Math.round(n).toLocaleString('pt-BR')};
  function countUp(el){
    if(el.dataset.done)return;el.dataset.done=1;
    var to=+el.dataset.count,suf=el.dataset.suffix||'';
    if(reduce){el.textContent=fmt(to)+suf;return}
    var t0=null,dur=1600;
    function step(t){if(!t0)t0=t;var p=Math.min((t-t0)/dur,1),e=1-Math.pow(1-p,4);el.textContent=fmt(to*e)+suf;if(p<1)requestAnimationFrame(step)}
    requestAnimationFrame(step);
  }

  // rolagem suave nas ancoras (compensa o menu fixo)
  function goTo(id){
    var t=id&&document.getElementById(id);if(!t)return false;
    window.scrollTo({top:t.getBoundingClientRect().top+window.pageYOffset-76,behavior:reduce?'auto':'smooth'});
    if(!t.hasAttribute('tabindex'))t.setAttribute('tabindex','-1');
    try{t.focus({preventScroll:true})}catch(x){t.focus()}
    return true;
  }
  q('a[href^="#"]',root).forEach(function(a){a.addEventListener('click',function(e){
    if(goTo(a.getAttribute('href').slice(1)))e.preventDefault();
  })});

  // nav + progresso + CTA fixo no mobile
  var nav=q('.bz-nav')[0],bar=q('.bz-progress')[0],mcta=q('#bz-mcta')[0],hero=q('.bz-hero')[0],formEl=q('#form')[0];
  function onScroll(){
    var y=window.pageYOffset,h=document.documentElement.scrollHeight-innerHeight;
    nav.classList.toggle('is-solid',y>30);bar.style.transform='scaleX('+(h>0?y/h:0)+')';
    if(mcta&&hero&&formEl){
      var hb=hero.getBoundingClientRect().bottom,fr=formEl.getBoundingClientRect();
      var on=hb<0&&!(fr.top<innerHeight&&fr.bottom>0);mcta.classList.toggle('is-on',on);mcta.setAttribute('aria-hidden',on?'false':'true')
    }
  }
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  // barra de abas dos modulos (fixa; so aparece dentro da area de modulos)
  var tabs=q('#bz-tabs')[0],tabA=tabs?q('a',tabs):[],tabS=tabA.map(function(a){return q(a.getAttribute('href'))[0]});
  function onTabs(){
    if(!tabs)return;
    var first=tabS[0],last=tabS[tabS.length-1];if(!first||!last)return;
    var fr=first.getBoundingClientRect(),lr=last.getBoundingClientRect();
    var on=fr.top<120&&lr.bottom>200;tabs.classList.toggle('is-on',on);
    var cur=0;tabS.forEach(function(s,i){if(s&&s.getBoundingClientRect().top<innerHeight*.45)cur=i});
    tabA.forEach(function(a,i){a.classList.toggle('is-on',i===cur);if(i===cur)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')})
  }
  addEventListener('scroll',onTabs,{passive:true});addEventListener('resize',onTabs);onTabs();

  // holofote do hero (so com mouse)
  var canHover=window.matchMedia&&matchMedia('(hover: hover)').matches;
  if(hero&&canHover&&!reduce){
    var spot=document.createElement('div');spot.className='bz-hero__spot';spot.setAttribute('aria-hidden','true');hero.insertBefore(spot,hero.firstChild);
    hero.addEventListener('mousemove',function(e){var r=hero.getBoundingClientRect();hero.style.setProperty('--mx',(e.clientX-r.left)+'px');hero.style.setProperty('--my',(e.clientY-r.top)+'px');hero.classList.add('is-spot')});
    hero.addEventListener('mouseleave',function(){hero.classList.remove('is-spot')});
  }
  // holofote nos blocos da faixa de IA
  if(canHover){q('.bz-aiband__ul li').forEach(function(c){c.addEventListener('mousemove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--x',(e.clientX-r.left)+'px');c.style.setProperty('--y',(e.clientY-r.top)+'px')})})}
  // titulo da faixa de IA acende palavra por palavra conforme a rolagem
  var say=q('.bz-aiband__t')[0];
  if(say){
    var words=[];
    Array.prototype.slice.call(say.childNodes).forEach(function(n){
      if(n.nodeType!==3)return;
      var frag=document.createDocumentFragment();
      n.textContent.split(/(\s+)/).forEach(function(t){if(!t)return;if(/^\s+$/.test(t)){frag.appendChild(document.createTextNode(t));return}var w=document.createElement('span');w.className='w';w.textContent=t;frag.appendChild(w);words.push(w)});
      say.replaceChild(frag,n);
    });
    var paint=function(){
      var r=say.getBoundingClientRect(),vh=innerHeight;
      var p=reduce?1:Math.min(1,Math.max(0,(vh*.85-r.top)/(vh*.4)));
      var k=Math.round(p*words.length);words.forEach(function(w,i){w.classList.toggle('on',i<k)});
    };
    paint();addEventListener('scroll',paint,{passive:true});
  }
  // botoes que levam ao formulario fazem ele "responder"
  var formBox=q('#form')[0];
  if(formBox&&!reduce){
    q('a[href="#form"]',root).forEach(function(a){a.addEventListener('click',function(){
      formBox.classList.remove('is-call');setTimeout(function(){void formBox.offsetWidth;formBox.classList.add('is-call')},650);
      setTimeout(function(){formBox.classList.remove('is-call')},1900);
    })});
  }

  // reveal + contadores
  var rv=q('.bz-rv,.bz-meter');
  function show(el){el.classList.add('is-in');q('[data-count]',el).forEach(countUp)}
  if('IntersectionObserver' in window&&!reduce){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){show(e.target);io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
    rv.forEach(function(el){io.observe(el)});
    q('.bz-hero__stats [data-count]').forEach(function(c){setTimeout(function(){countUp(c)},1100)});
  }else{rv.forEach(show);q('[data-count]').forEach(countUp)}

  // tilt 3D no card de preco
  q('[data-tilt]').forEach(function(el){
    if(reduce||matchMedia('(hover: none)').matches)return;
    el.addEventListener('pointermove',function(e){var r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;el.style.transform='perspective(900px) rotateY('+(x*10)+'deg) rotateX('+(-y*10)+'deg)'});
    el.addEventListener('pointerleave',function(){el.style.transform=''});
  });

  // pausa global de animacoes (WCAG 2.2.2)
  if(!reduce){
    var pb=document.createElement('button');pb.type='button';pb.className='bz-mctl';pb.setAttribute('aria-pressed','false');
    var IP='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>',IR='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>';
    pb.innerHTML=IP+'<span>Pausar animaciones</span>';
    pb.addEventListener('click',function(){var on=root.classList.toggle('is-paused');pb.setAttribute('aria-pressed',on);pb.innerHTML=(on?IR:IP)+'<span>Pausar animaciones</span>'});
    var sk=q('.bz-skip',root)[0];root.insertBefore(pb,sk?sk.nextSibling:root.firstChild);
  }

  // ---- hub de redes: esteira de chips + janela com o detalhe de cada rede ----
  var N=window.__BZ_NETS,hub=q('#redes')[0],rows=q('#bz-hub-rows')[0],dlg=q('#bz-netd')[0];
  if(N&&hub&&rows){
    var ids=N.order,rowDefs=[{off:0,rev:false,delay:0},{off:6,rev:true,delay:-34},{off:12,rev:false,delay:-67}];
    rowDefs.forEach(function(rd,ri){
      var ul=document.createElement('ul');ul.className='bz-hub__track'+(rd.rev?' bz-hub__track--rev':'');
      if(rd.delay)ul.style.animationDelay=rd.delay+'s';
      var seq=[];for(var j=0;j<ids.length;j++)seq.push(ids[(rd.off+j)%ids.length]);
      seq.splice(5,0,seq[14]);seq.splice(14,0,seq[3]);var dup={5:1,14:1};
      for(var pass=0;pass<2;pass++){
        for(var k=0;k<seq.length;k++){
          var id=seq[k],n=N.d[id],li=document.createElement("li"),b=document.createElement("button");
          b.type="button";b.className="bz-chip";b.setAttribute("data-net",id);b.setAttribute("aria-haspopup","dialog");
          b.setAttribute("aria-label",n.n+": ver cómo funciona Buzzmonitor");
          b.innerHTML="<span class=\"bz-chip__ic\"><img alt=\"\" width=\"26\" height=\"26\"></span><span></span>";
          b.querySelector("img").src=n.i;b.lastChild.textContent=n.n;
          if(pass||ri>0||dup[k]){li.setAttribute("aria-hidden","true");b.tabIndex=-1}
          li.appendChild(b);ul.appendChild(li);
        }
      }
      rows.appendChild(ul);
    });
    rows.addEventListener('focusin',function(e){var c=e.target.closest('.bz-chip');if(!c||c.tabIndex<0)return;var tr=c.closest('.bz-hub__track'),w=rows.clientWidth,off=c.parentNode.offsetLeft+c.offsetWidth/2-w/2;tr.style.animation='none';tr.style.transform='translateX('+(-Math.max(0,off))+'px)'});
    rows.addEventListener('focusout',function(e){if(rows.contains(e.relatedTarget))return;q('.bz-hub__track',rows).forEach(function(t){t.style.animation='';t.style.transform=''})});
    var cur=0,lastBtn=null;
    var byId=function(id){return document.getElementById(id)};
    var ICO_PUB='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>';
    var ICO_ADM='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>';
    function chip(txt,ico){var c=document.createElement('span');c.className='bz-netd__chip';c.innerHTML=ico;c.appendChild(document.createTextNode(txt));return c}
    function fill(i){
      cur=(i+ids.length)%ids.length;var id=ids[cur],n=N.d[id];
      byId('bz-netd-ic').src=n.i;byId('bz-netd-t').textContent=n.t;byId('bz-netd-lead').textContent=n.l;byId('bz-netd-time').textContent=n.m;
      var sc=byId('bz-netd-scope');sc.innerHTML='';
      if(n.e!=='adm')sc.appendChild(chip('Perfiles y términos públicos',ICO_PUB));
      if(n.e!=='pub')sc.appendChild(chip('Cuentas de tu marca',ICO_ADM));
      var ls=byId('bz-netd-list');ls.innerHTML='';
      n.it.forEach(function(it){var r=document.createElement('div');r.className='bz-netd__row';var l=document.createElement('span');l.className='bz-netd__lbl';l.textContent=it[0];var t=document.createElement('span');t.textContent=it[1];r.appendChild(l);r.appendChild(t);ls.appendChild(r)});
      var bd=dlg.querySelector('.bz-netd__body');if(bd)bd.scrollTop=0;
      if(window.dataLayer)window.dataLayer.push({event:'bzia_rede_aberta',rede:id});
    }
    function openNet(id,btn){
      hub.classList.add('is-stopped');lastBtn=btn||null;fill(Math.max(0,ids.indexOf(id)));
      if(typeof dlg.showModal==='function'){if(!dlg.open)dlg.showModal()}else dlg.setAttribute('open','');
      document.documentElement.style.overflow='hidden';
    }
    function cleanup(){document.documentElement.style.overflow="";hub.classList.remove("is-stopped");if(lastBtn&&document.contains(lastBtn)){try{lastBtn.focus({preventScroll:true})}catch(x){}}}
    function closeNet(){
      if(typeof dlg.close==="function"){if(dlg.open)dlg.close()}else dlg.removeAttribute("open");
      cleanup();
    }
    rows.addEventListener('click',function(e){var b=e.target.closest('.bz-chip');if(b){var id0=b.getAttribute('data-net');openNet(id0,rows.querySelector('.bz-hub__track:first-child .bz-chip[tabindex]:not([tabindex="-1"])[data-net="'+id0+'"]')||b)}});
    dlg.addEventListener("close",cleanup);
    dlg.addEventListener('click',function(e){
      if(e.target===dlg||e.target.closest('[data-netd-close]'))return closeNet();
      var st=e.target.closest('[data-netd-step]');if(st)return fill(cur+Number(st.getAttribute('data-netd-step')));
      if(e.target.closest('[data-netd-cta]')){e.preventDefault();lastBtn=null;closeNet();goTo('form')}
    });
    dlg.addEventListener('keydown',function(e){if(e.key==='ArrowRight')fill(cur+1);if(e.key==='ArrowLeft')fill(cur-1)});
  }

  // ---- pill tabs: nao ha nesta pagina ----

  // video: o YouTube so carrega no clique
  var vid=q('#bz-video')[0];
  if(vid){var vb=vid.querySelector('.bz-vid__poster');vb&&vb.addEventListener('click',function(){
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+vid.getAttribute('data-yt')+'?autoplay=1&rel=0&playsinline=1';
    f.title='Video de Buzzmonitor';
    f.setAttribute('allow','accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
    f.setAttribute('referrerpolicy','strict-origin-when-cross-origin');f.setAttribute('allowfullscreen','');
    vid.innerHTML='';vid.appendChild(f);try{f.focus()}catch(x){}
  })}

  // formulario: jsform da Jotform LATAM (241825239057661) direto no HTML, sem srcdoc
})();
