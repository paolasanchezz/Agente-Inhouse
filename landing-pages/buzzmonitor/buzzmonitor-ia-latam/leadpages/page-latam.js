
(function(){
// O reveal roda no CONTEUDO da secao, nunca na secao em si: com o empilhamento
// (stack) a secao precisa ficar 100% opaca o tempo todo, senao a secao fixada
// por baixo vaza atraves dela enquanto a de cima entra.
function reveal(){var els=[];Array.prototype.forEach.call(document.querySelectorAll('.bz-trusted,.bz-sec:not(.bz-sec-insights),.bz-testi,.bz-footerd'),function(s){Array.prototype.forEach.call(s.children,function(c){var t=c.tagName;if(t==='STYLE'||t==='SCRIPT'||t==='LINK')return;els.push(c);});});els.forEach(function(e){e.setAttribute('data-bzr','');});if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('bz-in');});return;}var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('bz-in');io.unobserve(x.target);}});},{threshold:0.12,rootMargin:'0px 0px -40px 0px'});els.forEach(function(e){io.observe(e);});}
// reveal por elemento: hero (fade-in up com stagger), grafismo (fade + escala)
// e a secao de insights (texto progressivo, imagem subindo ancorada na base).
// [sel, tipo, delay inicial em ms, incremento por ocorrencia]
function parts(){var groups=[['.bz-hero .bz-h1','up',0,0],['.bz-hero .bz-hero-desc','up',90,0],['.bz-hero .bz-form-ph','up',180,0],['.bz-hero-graphic','scale',120,0],['.bz-sec-insights .bz-pill','up',0,0],['.bz-sec-insights .bz-h2','up',80,0],['.bz-sec-insights .bz-feat-lead','up',160,0],['.bz-sec-insights .bz-body','up',240,90],['.bz-sec-insights .bz-ph-mock','base',140,0]];var all=[];groups.forEach(function(g){Array.prototype.forEach.call(document.querySelectorAll(g[0]),function(el,i){el.setAttribute('data-bzp',g[1]);el.style.transitionDelay=(g[2]+i*g[3])+'ms';all.push(el);});});function showAll(){all.forEach(function(e){e.classList.add('bz-in');});}
try{if(!('IntersectionObserver' in window)){showAll();return;}var iop=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('bz-in');iop.unobserve(x.target);}});},{threshold:0,rootMargin:'0px 0px -10% 0px'});all.forEach(function(e){iop.observe(e);});}catch(err){showAll();}}
function marquee(){var row=document.querySelector('.bz-trusted .bz-logos-row');if(!row||row.dataset.bzMarquee)return;row.dataset.bzMarquee='1';var items=Array.prototype.slice.call(row.children);var track=document.createElement('div');track.className='bz-marquee-track';items.forEach(function(el){track.appendChild(el);});items.forEach(function(el){var c=el.cloneNode(true);c.setAttribute('aria-hidden','true');track.appendChild(c);});row.appendChild(track);}
// accordion da secao "Uma so plataforma": altura exata via scrollHeight (easing
// certo em qualquer texto) e aria-expanded espelhando o estado.
function accordion(){Array.prototype.forEach.call(document.querySelectorAll('.bz-benefits .bz-benefit'),function(it){var btn=it.querySelector('.bz-acc-btn'),panel=it.querySelector('.bz-acc-panel');if(!btn||!panel)return;btn.addEventListener('click',function(){var open=!it.classList.contains('is-open');it.classList.toggle('is-open',open);btn.setAttribute('aria-expanded',open?'true':'false');panel.style.maxHeight=open?panel.scrollHeight+'px':'0px';});});
window.addEventListener('resize',function(){Array.prototype.forEach.call(document.querySelectorAll('.bz-benefit.is-open .bz-acc-panel'),function(p){p.style.maxHeight=p.scrollHeight+'px';});});}
// empilhamento das secoes no scroll
// O hero fica FORA do empilhamento de proposito: o formulario (#form-demo) mora
// nele, e hero sticky deixa o alvo permanentemente "visivel" pro browser — a
// ancora do CTA para de sair do lugar e o form fica coberto pelas secoes de cima.
// Fora do stack, o hero rola normal, a ancora volta a funcionar nativamente e o
// empilhamento segue valendo da segunda secao em diante.
function stack(){var nav=document.querySelector('.bz-nav');var secs=Array.prototype.slice.call(document.querySelectorAll('body > section:not(.bz-nav):not(.bz-hero)'));if(!secs.length)return;secs.forEach(function(s,i){s.classList.add('bz-stack');s.style.zIndex=String(i+1);});
function fit(){var navH=nav?nav.offsetHeight:0,vh=window.innerHeight;secs.forEach(function(s){s.style.top=Math.min(navH,vh-s.offsetHeight)+'px';});}
fit();window.addEventListener('resize',fit);window.addEventListener('load',fit);
if('ResizeObserver' in window){var ro=new ResizeObserver(fit);secs.forEach(function(s){ro.observe(s);});}}
function init(){reveal();parts();marquee();accordion();stack();}
if(document.readyState!=='loading'){init();}else{document.addEventListener('DOMContentLoaded',init);}
})();
