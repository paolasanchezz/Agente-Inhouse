/* ==========================================================================
   Café con Cxpress · Medellín · 24/09/2026
   JavaScript vanilla, sin dependencias. Todo degrada con gracia:
   si el script no corre, el texto ya está visible (.reveal en <noscript>)
   y el bloque de cuenta regresiva simplemente no se anima.
   ========================================================================== */
(function () {
  'use strict';

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  /* ---------- 1. Reveal on scroll ---------- */
  var reveals = document.querySelectorAll('.reveal');

  if (reduce || !hasIO) {
    for (var i = 0; i < reveals.length; i++) {
      reveals[i].classList.add('in');
    }
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    for (var j = 0; j < reveals.length; j++) {
      io.observe(reveals[j]);
    }
  }

  /* ---------- 2. Cuenta regresiva ----------
     Evento: 24 de septiembre de 2026, 4:00 p.m. hora de Colombia (UTC-5).
     El contenedor lleva aria-hidden="true": la fecha ya vive en la copy del
     hero y en el JSON-LD, y un contador que cambia cada segundo inunda los
     lectores de pantalla (WCAG 2.2.2 / GUIDELINES 7). */
  var TARGET = new Date('2026-09-24T16:00:00-05:00').getTime();

  var box = document.getElementById('countdown');
  var elDays = document.getElementById('cd-days');
  var elHours = document.getElementById('cd-hours');
  var elMins = document.getElementById('cd-mins');
  var elSecs = document.getElementById('cd-secs');

  function pad(n) {
    return n < 10 ? '0' + n : String(n);
  }

  function tick() {
    var diff = TARGET - Date.now();

    if (diff <= 0) {
      if (box) { box.textContent = ''; }
      return false;
    }

    var secs = Math.floor(diff / 1000);
    elDays.textContent = pad(Math.floor(secs / 86400));
    elHours.textContent = pad(Math.floor(secs / 3600) % 24);
    elMins.textContent = pad(Math.floor(secs / 60) % 60);
    elSecs.textContent = pad(secs % 60);
    return true;
  }

  if (box && elDays && elHours && elMins && elSecs) {
    if (tick()) {
      var timer = setInterval(function () {
        if (!tick()) { clearInterval(timer); }
      }, 1000);
    }
  }

  /* El formulario es un embed de Jotform (jsform 261303944881662), que se
     renderiza en su propio iframe. No hay handler de submit aquí: el mock y su
     listener salieron al integrar el embed real (lp-integrar-form, Paso 2.5),
     porque el form ya no existe en el DOM de esta página y el listener rompía. */
})();
