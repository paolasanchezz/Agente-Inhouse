(function(){
  var q=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
  var root=q('#bzm')[0];if(!root)return;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  // O editor da Leadpages roda estes scripts (blob:) e grava no HTML o que eles injetam. Nele, nada e injetado.
  var editor=/^(blob|about):/.test(location.protocol)||(location.ancestorOrigins&&location.ancestorOrigins.length>0&&/(^|\.)leadpages\.com$/.test((location.ancestorOrigins[0]||'').replace(/^https?:\/\//,'')));
  q('.bz-mctl',root).forEach(function(el){el.parentNode.removeChild(el)});
  root.classList.remove('is-paused');
  if(editor){root.classList.remove('js');root.classList.add('is-editor');return}
  root.classList.remove('is-editor');
  root.classList.add('js');

  var fmt=function(n){return Math.round(n).toLocaleString('es-MX')};
  function countUp(el){
    if(el.dataset.done)return;el.dataset.done=1;if(reduce)return;
    var to=+el.dataset.count,t0=null,dur=1600;
    function step(t){if(!t0)t0=t;var p=Math.min((t-t0)/dur,1),e=1-Math.pow(1-p,4);el.textContent=fmt(to*e);if(p<1)requestAnimationFrame(step)}
    requestAnimationFrame(step);
  }

  // rolagem suave nas ancoras (compensa o menu fixo)
  q('a[href^="#"]',root).forEach(function(a){a.addEventListener('click',function(e){
    var id=a.getAttribute('href').slice(1),t=id&&document.getElementById(id);if(!t)return;
    e.preventDefault();window.scrollTo({top:t.getBoundingClientRect().top+window.pageYOffset-76,behavior:reduce?'auto':'smooth'});
    if(!t.hasAttribute('tabindex'))t.setAttribute('tabindex','-1');
    try{t.focus({preventScroll:true})}catch(x){t.focus()}
  })});

  // nav + progresso
  var nav=q('.bz-nav')[0],bar=q('.bz-progress')[0];
  function onScroll(){var y=window.pageYOffset,h=document.documentElement.scrollHeight-innerHeight;nav.classList.toggle('is-solid',y>30);bar.style.transform='scaleX('+(h>0?y/h:0)+')'}
  addEventListener('scroll',onScroll,{passive:true});onScroll();

  // reveal + contador do preco
  var rv=q('.bz-rv,.bz-meter');
  function show(el){el.classList.add('is-in');q('[data-count]',el).forEach(countUp)}
  if('IntersectionObserver' in window&&!reduce){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){show(e.target);io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
    rv.forEach(function(el){io.observe(el)});
  }else rv.forEach(show);

  // tilt 3D no card de preco (mesmo efeito da LP de referencia)
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

  // pill tabs
  var tabs=q('.bz-pt__btn'),panels=q('.bz-pt__panel'),pill=q('.bz-pt__pill')[0],barEl=q('.bz-pt__bar')[0];
  function sel(){return tabs.filter(function(t){return t.getAttribute('aria-selected')==='true'})[0]||tabs[0]}
  function place(t){pill.style.width=t.offsetWidth+'px';pill.style.transform='translateX('+t.offsetLeft+'px)'}
  function pick(i,focus){
    tabs.forEach(function(t,n){var on=n===i;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1});
    panels.forEach(function(p,n){var on=n===i;p.classList.toggle('is-on',on);if(on)p.removeAttribute('hidden');else p.setAttribute('hidden','')});
    place(tabs[i]);
    var t=tabs[i];if(barEl.scrollWidth>barEl.clientWidth)barEl.scrollTo({left:t.offsetLeft-20,behavior:reduce?'auto':'smooth'});
    if(focus)t.focus();
  }
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){pick(i)});
    t.addEventListener('keydown',function(e){
      var k=e.key,n=i;
      if(k==='ArrowRight')n=(i+1)%tabs.length;else if(k==='ArrowLeft')n=(i-1+tabs.length)%tabs.length;else if(k==='Home')n=0;else if(k==='End')n=tabs.length-1;else return;
      e.preventDefault();pick(n,true);
    });
  });
  var wrapEl=q('.bz-pt__wrap')[0],navL=q('.bz-pt__nav--l')[0],navR=q('.bz-pt__nav--r')[0];
  function edges(){
    var o=barEl.scrollWidth>barEl.clientWidth+2;
    wrapEl.classList.toggle('is-scroll',o);
    wrapEl.classList.toggle('can-l',o&&barEl.scrollLeft>4);
    wrapEl.classList.toggle('can-r',o&&barEl.scrollLeft<barEl.scrollWidth-barEl.clientWidth-4);
  }
  barEl.addEventListener('scroll',edges,{passive:true});
  navL.addEventListener('click',function(){barEl.scrollBy({left:-180,behavior:reduce?'auto':'smooth'})});
  navR.addEventListener('click',function(){barEl.scrollBy({left:180,behavior:reduce?'auto':'smooth'})});
  place(sel());edges();addEventListener('resize',function(){place(sel());edges()});
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){place(sel());edges()});

})();