/* =========================================================================
   Garage Mecanochris — JavaScript
   Vanilla, sans dépendance, sans étape de build.
   ========================================================================= */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- En-tête : ombre une fois défilé ---------------------------------- */
  (function stickyHead() {
    var head = document.querySelector('.site-head');
    if (!head) return;
    var tick = false;
    function update() {
      head.setAttribute('data-stuck', window.scrollY > 8 ? 'true' : 'false');
      tick = false;
    }
    window.addEventListener('scroll', function () {
      if (!tick) { tick = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    update();
  })();

  /* --- Menu mobile ------------------------------------------------------ */
  (function mobileNav() {
    var burger = document.querySelector('.burger');
    var nav = document.getElementById('nav-principal');
    if (!burger || !nav) return;

    function close() {
      burger.setAttribute('aria-expanded', 'false');
      nav.setAttribute('data-open', 'false');
    }
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      nav.setAttribute('data-open', String(!open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') {
        close();
        burger.focus();
      }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 900) close();
    });
  })();

  /* --- Index des services : l'image suit le curseur --------------------- */
  (function servicePreview() {
    var list = document.querySelector('[data-preview-list]');
    if (!list || reduced) return;
    if (!window.matchMedia('(hover: hover) and (min-width: 901px)').matches) return;

    var box = document.createElement('div');
    box.className = 'preview';
    box.setAttribute('aria-hidden', 'true');
    var img = document.createElement('img');
    img.alt = '';
    img.decoding = 'async';
    box.appendChild(img);
    document.body.appendChild(box);

    var tx = 0, ty = 0, cx = 0, cy = 0, running = false, current = null;

    function loop() {
      cx += (tx - cx) * 0.12;
      cy += (ty - cy) * 0.12;
      box.style.transform = 'translate3d(' + cx + 'px,' + cy + 'px,0) scale(' +
        (box.getAttribute('data-on') === 'true' ? 1 : 0.9) + ')';
      if (running) window.requestAnimationFrame(loop);
    }

    list.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse') return;
      tx = e.clientX + 150;
      ty = e.clientY;
    });

    list.querySelectorAll('[data-preview]').forEach(function (link) {
      link.addEventListener('pointerenter', function (e) {
        if (e.pointerType !== 'mouse') return;
        var src = link.getAttribute('data-preview');
        if (src !== current) { img.src = src; current = src; }
        tx = e.clientX + 150; ty = e.clientY;
        if (!running) { cx = tx; cy = ty; running = true; window.requestAnimationFrame(loop); }
        box.setAttribute('data-on', 'true');
      });
    });

    list.addEventListener('pointerleave', function () {
      box.setAttribute('data-on', 'false');
      window.setTimeout(function () {
        if (box.getAttribute('data-on') === 'false') running = false;
      }, 400);
    });
  })();

  /* --- Apparition en défilement (retenue : intertitres et panneaux) ----- */
  (function reveal() {
    var items = document.querySelectorAll('.reveal');
    if (!items.length) return;
    if (reduced || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.setAttribute('data-seen', 'true'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.setAttribute('data-seen', 'true');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  })();

  /* --- Ouvert / fermé en direct (lun–ven 08 h–17 h, Europe/Brussels) ---- */
  (function openState() {
    var nodes = document.querySelectorAll('[data-open-state]');
    if (!nodes.length) return;

    var now;
    try {
      now = new Date(new Date().toLocaleString('en-US', { timeZone: 'Europe/Brussels' }));
    } catch (err) {
      now = new Date();
    }
    var day = now.getDay();            // 0 = dimanche
    var minutes = now.getHours() * 60 + now.getMinutes();
    var weekday = day >= 1 && day <= 5;
    var open = weekday && minutes >= 8 * 60 && minutes < 17 * 60;

    var label;
    if (open) {
      label = 'Ouvert maintenant · jusqu’à 17 h';
    } else if (weekday && minutes < 8 * 60) {
      label = 'Fermé · ouvre à 8 h';
    } else if (weekday) {
      label = day === 5 ? 'Fermé · ouvre lundi à 8 h' : 'Fermé · ouvre demain à 8 h';
    } else {
      label = 'Fermé le week-end · ouvre lundi à 8 h';
    }

    nodes.forEach(function (node) {
      node.textContent = label;
      node.setAttribute('data-state', open ? 'open' : 'closed');
    });
  })();

  /* --- Année courante --------------------------------------------------- */
  (function year() {
    var el = document.querySelector('[data-year]');
    if (el) el.textContent = String(new Date().getFullYear());
  })();

  /* --- Formulaire de contact -------------------------------------------- */
  (function contactForm() {
    var form = document.querySelector('[data-contact-form]');
    if (!form) return;

    var status = form.querySelector('.form-status');
    var submit = form.querySelector('button[type="submit"]');
    var endpoint = form.getAttribute('action') || '';
    var keyField = form.querySelector('input[name="access_key"]');
    var key = keyField ? keyField.value.trim() : '';
    var configured = endpoint.indexOf('http') === 0 && key.indexOf('VOTRE_CLE') === -1 && key.length > 12;

    function fieldOf(input) { return input.closest('.field'); }

    function message(input) {
      if (input.validity.valueMissing) {
        return input.type === 'email'
          ? 'Indiquez votre adresse e-mail pour que nous puissions vous répondre.'
          : 'Ce champ est nécessaire pour traiter votre demande.';
      }
      if (input.validity.typeMismatch && input.type === 'email') {
        return 'Cette adresse e-mail semble incomplète — vérifiez le « @ » et le domaine.';
      }
      if (input.validity.tooShort) {
        return 'Ajoutez encore quelques mots (' + input.minLength + ' caractères minimum).';
      }
      return 'Cette valeur n’est pas valide.';
    }

    function check(input) {
      var wrap = fieldOf(input);
      if (!wrap) return input.checkValidity();
      var ok = input.checkValidity();
      wrap.setAttribute('data-invalid', ok ? 'false' : 'true');
      input.setAttribute('aria-invalid', ok ? 'false' : 'true');
      var box = wrap.querySelector('.field-error');
      if (box && !ok) box.textContent = message(input);
      return ok;
    }

    form.querySelectorAll('input, textarea, select').forEach(function (input) {
      input.addEventListener('blur', function () { check(input); });
      input.addEventListener('input', function () {
        if (fieldOf(input) && fieldOf(input).getAttribute('data-invalid') === 'true') check(input);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var valid = true;
      var first = null;
      form.querySelectorAll('input, textarea, select').forEach(function (input) {
        if (!check(input)) { valid = false; if (!first) first = input; }
      });
      if (!valid) {
        status.setAttribute('data-state', 'error');
        status.textContent = 'Quelques champs sont à compléter avant l’envoi.';
        if (first) first.focus();
        return;
      }

      if (!configured) {
        status.setAttribute('data-state', 'error');
        status.textContent =
          'Formulaire non encore connecté : ajoutez votre clé Web3Forms dans le champ ' +
          '« access_key » de contact.html. En attendant, appelez le 071 88 56 83.';
        return;
      }

      submit.setAttribute('aria-busy', 'true');
      submit.disabled = true;
      status.setAttribute('data-state', 'ok');
      status.textContent = 'Envoi en cours…';

      fetch(endpoint, {
        method: 'POST',
        headers: { Accept: 'application/json' },
        body: new FormData(form)
      })
        .then(function (res) { return res.ok ? res : Promise.reject(res); })
        .then(function () {
          form.reset();
          status.setAttribute('data-state', 'ok');
          status.textContent =
            'Merci, votre demande est bien partie. Nous vous répondons pendant les heures d’atelier, ' +
            'du lundi au vendredi de 8 h à 17 h.';
        })
        .catch(function () {
          status.setAttribute('data-state', 'error');
          status.textContent =
            'L’envoi n’a pas abouti. Appelez-nous au 071 88 56 83 ou écrivez à info@mecanochris.be.';
        })
        .then(function () {
          submit.removeAttribute('aria-busy');
          submit.disabled = false;
        });
    });
  })();

  /* --- Recherche pneus : démonstration, sans partenaire connecté -------- */
  (function tyreDemo() {
    var form = document.querySelector('[data-tyre-form]');
    if (!form) return;
    var out = form.querySelector('.form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      out.setAttribute('data-state', 'ok');
      out.textContent =
        'Dimension ' + (d.get('largeur') || '—') + '/' + (d.get('hauteur') || '—') +
        ' R' + (d.get('diametre') || '—') + ' — saison : ' + (d.get('saison') || '—') + '. ' +
        'La recherche en direct passe par notre partenaire ; appelez le 071 88 56 83 pour un prix posé, monté et équilibré.';
    });
  })();
})();
