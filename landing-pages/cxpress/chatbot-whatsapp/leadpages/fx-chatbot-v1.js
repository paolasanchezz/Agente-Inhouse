(function(){
  /* Camada de movimento v1: titulo por palavras, luz do mouse nos cards e frase que acende com a rolagem.
     Nao roda no editor da Leadpages (blob:/leadpages.com): la o DOM injetado seria gravado na pagina.
     Com prefers-reduced-motion nada anima. */
  var mm = window.matchMedia;
  if(!mm || mm('(prefers-reduced-motion: reduce)').matches) return;
  if(/^(blob|about):/.test(location.protocol) || /(^|\.)leadpages\.com$/.test(location.hostname)) return;
  function wrap(node, list, cls){
    Array.prototype.slice.call(node.childNodes).forEach(function(n){
      if(n.nodeType === 3){
        var frag = document.createDocumentFragment();
        n.nodeValue.split(/(\s+)/).forEach(function(t){
          if(!t) return;
          if(/^\s+$/.test(t)){ frag.appendChild(document.createTextNode(t)); return; }
          var s = document.createElement('span'); s.className = cls; s.textContent = t;
          list.push(s); frag.appendChild(s);
        });
        node.replaceChild(frag, n);
      } else if(n.nodeType === 1){ wrap(n, list, cls); }
    });
  }
  if(mm('(hover: hover)').matches){
    document.querySelectorAll('.why-card,.proof__item,.feat').forEach(function(c){
      c.addEventListener('mousemove', function(e){
        var r = c.getBoundingClientRect();
        c.style.setProperty('--x', (e.clientX - r.left) + 'px');
        c.style.setProperty('--y', (e.clientY - r.top) + 'px');
      });
    });
  }
  var h2 = document.querySelector('.why__head h2');
  if(h2){
    var words = [];
    wrap(h2, words, 'w');
    h2.classList.add('lit');
    var tick = false;
    var paint = function(){
      tick = false;
      var r = h2.getBoundingClientRect(), vh = window.innerHeight || 800;
      var p = Math.min(1, Math.max(0, (vh*.88 - r.top) / (r.height + vh*.3)));
      var n = Math.round(p * words.length);
      words.forEach(function(w, i){ w.classList.toggle('on', i < n); });
    };
    window.addEventListener('scroll', function(){ if(!tick){ tick = true; requestAnimationFrame(paint); } }, {passive:true});
    window.addEventListener('resize', paint);
    paint();
  }
})();
