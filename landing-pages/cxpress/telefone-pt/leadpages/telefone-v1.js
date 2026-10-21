/* Cxpress PT-PT · telefone-pt · v1 */
(function(){
'use strict';
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
window.__paused=false;
if(window.matchMedia){var mq=matchMedia('(prefers-reduced-motion: reduce)');if(mq.addEventListener)mq.addEventListener('change',function(e){if(e.matches){window.__paused=true;document.documentElement.classList.add('anim-paused')}})}
var $=function(s,c){return (c||document).querySelector(s)};
var $$=function(s,c){return [].slice.call((c||document).querySelectorAll(s))};
function onView(el,cb,margin){
  if(!('IntersectionObserver' in window)){cb(true);return}
  new IntersectionObserver(function(es){es.forEach(function(e){cb(e.isIntersecting)})},{rootMargin:margin||'0px'}).observe(el);
}

/* revelar ao rolar + contadores */
(function(){
  var rv=$$('.reveal');
  if(!('IntersectionObserver' in window)||reduce){rv.forEach(function(e){e.classList.add('is-visible')});}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -40px 0px'});rv.forEach(function(e){io.observe(e)});}
  $$('[data-count]').forEach(function(el){
    var to=parseFloat(el.getAttribute('data-count')),done=false;
    function run(){if(done)return;done=true;if(reduce){el.firstChild.nodeValue=to;return}
      var t0=performance.now();(function f(t){var p=Math.min(1,(t-t0)/1100),v=Math.round(to*(1-Math.pow(1-p,3)));el.firstChild.nodeValue=v;if(p<1)requestAnimationFrame(f)})(t0)}
    onView(el,function(v){if(v)run()});
  });
})();

/* cabeçalho + link ativo */
(function(){
  var nav=$('.navbar');
  function s(){nav.classList.toggle('is-solid',window.scrollY>30)}
  window.addEventListener('scroll',s,{passive:true});s();
  var links=$$('.navbar__links a'),map=links.map(function(a){return $(a.getAttribute('href'))});
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var i=map.indexOf(e.target);links.forEach(function(l,j){l.classList.toggle('is-on',j===i);if(j===i)l.setAttribute('aria-current','true');else l.removeAttribute('aria-current')})}})},{rootMargin:'-45% 0px -50% 0px'});
    map.forEach(function(m){if(m)io.observe(m)});
  }
})();

/* rede de pontos no hero */
(function(){
  var c=$('#net');if(!c||reduce)return;
  var x=c.getContext('2d'),W,H,pts=[],vis=true,dpr=Math.min(2,window.devicePixelRatio||1);
  function size(){var r=c.getBoundingClientRect();W=r.width;H=r.height;c.width=W*dpr;c.height=H*dpr;x.setTransform(dpr,0,0,dpr,0,0);
    var n=Math.round(Math.min(60,W*H/22000));pts=[];for(var i=0;i<n;i++)pts.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.28,vy:(Math.random()-.5)*.28})}
  size();window.addEventListener('resize',size);
  onView(c,function(v){vis=v;if(v)loop()});
  var run=false;
  function loop(){if(run)return;run=true;(function f(){if(!vis){run=false;return}
    x.clearRect(0,0,W,H);
    for(var i=0;i<pts.length;i++){var p=pts[i];if(!window.__paused){p.x+=p.vx;p.y+=p.vy}if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;
      for(var j=i+1;j<pts.length;j++){var q=pts[j],dx=p.x-q.x,dy=p.y-q.y,d=dx*dx+dy*dy;if(d<17000){x.strokeStyle='rgba(157,182,255,'+(.32*(1-d/17000))+')';x.lineWidth=1;x.beginPath();x.moveTo(p.x,p.y);x.lineTo(q.x,q.y);x.stroke()}}
      x.fillStyle='rgba(207,217,255,.75)';x.beginPath();x.arc(p.x,p.y,1.6,0,6.3);x.fill()}
    requestAnimationFrame(f)})()}
})();

/* construtor do diagrama de encaminhamento (usado no palco e no cartão interativo) */
var NS='http://www.w3.org/2000/svg';
function el(n,a,p){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
function buildRoute(host,labels){
  var svg=el('svg',{viewBox:'0 0 480 230',role:'img','aria-label':'Diagrama: o voicebot recebe a chamada e encaminha-a para a fila de '+labels.join(', ')}),
      paths=[],nodes=[],ys=[40,115,190];
  var src=el('g',{'class':'rt-node rt-src'},svg);
  el('rect',{x:10,y:84,width:128,height:62,rx:14},src);
  var t=el('text',{x:74,y:112,'text-anchor':'middle'},src);t.textContent='Voicebot';
  var s2=el('text',{x:74,y:131,'text-anchor':'middle','class':'sub'},src);s2.textContent='1.º nível · IA';
  labels.forEach(function(l,i){
    var y=ys[i];
    var d='M138 115 C 230 115, 230 '+y+', 330 '+y;
    paths.push(el('path',{d:d,'class':'rt-path'},svg));
    var g=el('g',{'class':'rt-node'},svg);
    el('rect',{x:330,y:y-26,width:140,height:52,rx:13},g);
    var a=el('text',{x:400,y:y+1,'text-anchor':'middle'},g);a.textContent=l;
    var b=el('text',{x:400,y:y+16,'text-anchor':'middle','class':'sub'},g);b.textContent=['fila · 3 agentes','fila · 5 agentes','fila · 2 agentes'][i];
    nodes.push(g);
  });
  var dot=el('circle',{r:7,'class':'rt-dot',cx:-20,cy:-20},svg);
  var anim=el('animateMotion',{dur:'1.1s',fill:'freeze',begin:'indefinite',calcMode:'spline',keyTimes:'0;1',keySplines:'.4 0 .2 1'},dot);
  host.appendChild(svg);
  var cur=-1;
  function go(i){
    if(i===cur&&!reduce){}
    cur=i;
    paths.forEach(function(p,k){p.classList.toggle('is-hot',k===i)});
    nodes.forEach(function(n,k){n.classList.remove('is-hot');if(k===i)setTimeout(function(){n.classList.add('is-hot')},reduce?0:900)});
    anim.setAttribute('path',paths[i].getAttribute('d'));
    if(!reduce&&anim.beginElement){try{anim.beginElement()}catch(e){}}else{dot.setAttribute('cx',330);dot.setAttribute('cy',ys[i]);dot.removeAttribute('transform')}
  }
  return {go:go,reset:function(){cur=-1;paths.forEach(function(p){p.classList.remove('is-hot')});nodes.forEach(function(n){n.classList.remove('is-hot')});dot.setAttribute('cx',-20);dot.setAttribute('cy',-20)}};
}

/* palco: cena de 15 s em loop */
(function(){
  var st=$('#stage');if(!st)return;
  var scenes=$$('.scene',st),chaps=$$('.chap',st),timeEl=$('#stTime'),TOTAL=15000,SC=3000;
  var rt=buildRoute($('#stageRoute'),['Vendas','Apoio','Agendamentos']);
  var cur=-1,t0=performance.now(),offset=0,playing=true,visible=true,timers=[];
  function clearT(){timers.forEach(clearTimeout);timers=[]}
  function later(fn,ms){timers.push(setTimeout(fn,ms))}
  function tn(node){if(node.lastChild.nodeType!==3)node.appendChild(document.createTextNode(''));return node.lastChild}
  function type(node,text,speed,cb){
    var T=tn(node);node.classList.add('is-on','caret');T.nodeValue='';var i=0;
    (function f(){T.nodeValue=text.slice(0,++i);if(i<text.length)timers.push(setTimeout(f,speed));else{node.classList.remove('caret');if(cb)cb()}})();
  }
  function enter(i){
    clearT();
    scenes.forEach(function(s,k){s.classList.toggle('is-active',k===i);s.setAttribute('aria-hidden',k===i?'false':'true')});
    chaps.forEach(function(c,k){c.classList.toggle('is-active',k===i);c.classList.toggle('is-done',k<i);c.setAttribute('aria-current',k===i?'step':'false')});
    if(i===1){
      var a=$('#tl1'),b=$('#tl2'),n=$('#intent');[a,b].forEach(function(x){x.classList.remove('is-on','caret');tn(x).nodeValue=''});n.classList.remove('is-on');
      if(reduce){a.classList.add('is-on');tn(a).nodeValue=a.getAttribute('data-t');b.classList.add('is-on');tn(b).nodeValue=b.getAttribute('data-t');n.classList.add('is-on')}
      else{later(function(){type(a,a.getAttribute('data-t'),28,function(){later(function(){type(b,b.getAttribute('data-t'),24,function(){later(function(){n.classList.add('is-on')},250)})},350)})},200)}
    }
    if(i===2){rt.reset();later(function(){rt.go(2)},reduce?0:450)}
    if(i===3){var k=$('#kpiA');var to=128,t1=performance.now();if(reduce)k.firstChild.nodeValue=to;else(function f(t){var p=Math.min(1,(t-t1)/1300);k.firstChild.nodeValue=Math.round(to*(1-Math.pow(1-p,3)));if(p<1&&cur===3)requestAnimationFrame(f)})(t1)}
  }
  function seek(ms){offset=ms;t0=performance.now()}
  chaps.forEach(function(c,k){c.addEventListener('click',function(){seek(k*SC);tick(true)})});
  function tick(force){
    var e=((performance.now()-t0)+offset)%TOTAL,i=Math.floor(e/SC);
    if(i!==cur||force){cur=i;enter(i)}
    var inScene=(e%SC)/SC;
    chaps.forEach(function(c,k){var f=c.querySelector('span i');if(f)f.style.width=(k<i?100:k===i?inScene*100:0)+'%'});
    var s=Math.floor(e/1000);timeEl.textContent='00:'+(s<10?'0':'')+s;
  }
  if(reduce){var pb=$('#pauseBtn');if(pb)pb.hidden=true;cur=2;enter(2);chaps.forEach(function(c,k){c.addEventListener('click',function(){cur=k;enter(k)})});return}
  var pauseBtn=$('#pauseBtn'),pausedAt=0;
  function setPaused(v){
    if(v===window.__paused)return;window.__paused=v;
    document.documentElement.classList.toggle('anim-paused',v);
    if(v){pausedAt=performance.now()}else{t0+=performance.now()-pausedAt}
    if(pauseBtn){pauseBtn.setAttribute('aria-pressed',v?'true':'false');pauseBtn.querySelector('span').textContent=v?'Retomar animação':'Pausar animação'}
  }
  if(pauseBtn)pauseBtn.addEventListener('click',function(){setPaused(!window.__paused)});
  st.addEventListener('focusin',function(e){if(e.target.closest&&e.target.closest('.chap'))setPaused(true)});
  (function loop(){if(playing&&visible&&!window.__paused)tick();requestAnimationFrame(loop)})();
  onView(st,function(v){visible=v;if(v){t0=performance.now()-0;}},'0px');
  document.addEventListener('visibilitychange',function(){playing=!document.hidden;if(playing)seek(((performance.now()-t0)+offset)%TOTAL)});
  /* leve inclinação 3D com o rato */
  if(window.matchMedia('(hover:hover)').matches){
    var hero=$('.hero');
    hero.addEventListener('mousemove',function(e){if(window.__paused||e.target.closest('.stage__chapters'))return;var r=st.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;
      st.style.transform='perspective(1100px) rotateY('+(((e.clientX-cx)/innerWidth)*7).toFixed(2)+'deg) rotateX('+((-(e.clientY-cy)/innerHeight)*6).toFixed(2)+'deg)'});
    hero.addEventListener('mouseleave',function(){st.style.transform=''});
  }
})();

/* cartão de distribuição: o utilizador escolhe o motivo da chamada */
(function(){
  var host=$('#cardRoute');if(!host)return;
  var rt=buildRoute(host,['Vendas','Apoio','Agendamentos']);
  var btns=$$('.qbtn');
  function pick(i){btns.forEach(function(b,k){b.setAttribute('aria-pressed',k===i?'true':'false')});rt.go(i)}
  btns.forEach(function(b,k){b.addEventListener('click',function(){pick(k);auto=false})});
  var auto=true;
  onView(host,function(v){if(v&&auto){auto=false;setTimeout(function(){pick(0)},400)}});
})();

/* dispositivos */
(function(){
  var tabs=$$('.devtabs button'),svgs=$$('.dev svg');if(!tabs.length)return;
  var auto=true,i=0;
  function sel(k){i=k;tabs.forEach(function(t,j){t.setAttribute('aria-pressed',j===k?'true':'false')});svgs.forEach(function(s,j){s.classList.toggle('is-on',j===k)})}
  tabs.forEach(function(t,k){t.addEventListener('click',function(){auto=false;sel(k)})});
  sel(0);
  var box=$('.devtabs');box.addEventListener('mouseenter',function(){auto=false});box.addEventListener('focusin',function(){auto=false});
  if(!reduce)setInterval(function(){if(auto&&!window.__paused)sel((i+1)%tabs.length)},3200);
})();

/* gravação */
(function(){
  var b=$('#recBtn');if(!b)return;
  var w=$('#recWave'),tm=$('#recTime'),on=false,t,sec=0;
  var P='<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>',S='<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg>';
  function stop(){on=false;clearInterval(t);w.classList.remove('is-live');b.innerHTML=P;b.setAttribute('aria-label','Simular a reprodução de uma gravação')}
  b.addEventListener('click',function(){
    if(on){stop();return}
    on=true;sec=0;w.classList.add('is-live');b.innerHTML=S;b.setAttribute('aria-label','Parar a simulação');
    t=setInterval(function(){sec++;tm.textContent='00:0'+Math.min(sec,9)+' / 02:41';if(sec>=8)stop()},1000);
  });
})();

/* ondas: alturas variadas */
$$('.wave').forEach(function(w){var n=w.getAttribute('data-n')||30;for(var i=0;i<n;i++){var b=document.createElement('i');b.style.setProperty('--i',i);b.style.setProperty('--h',(.25+Math.abs(Math.sin(i*1.7)*Math.cos(i*.6))*.75).toFixed(2));w.appendChild(b)}});

/* barras de dashboard (cartão, sem palco) */
$$('.vis .bars').forEach(function(b){onView(b,function(v){if(v)b.classList.add('is-in')})});

/* holofote nos cartões */
if(window.matchMedia('(hover:hover)').matches){
  $$('.bcard').forEach(function(c){c.addEventListener('mousemove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-r.left)+'px');c.style.setProperty('--my',(e.clientY-r.top)+'px')})});
}

})();
