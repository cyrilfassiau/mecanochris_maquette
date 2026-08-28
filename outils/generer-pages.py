# -*- coding: utf-8 -*-
"""Régénère les six pages statiques depuis un gabarit unique.

FACULTATIF. Le livrable est le HTML déjà écrit à la racine : il fonctionne sans
ce script. Utilisez-le seulement pour éviter de recopier l'en-tête et le pied de
page à la main dans les six fichiers.

    python3 outils/generer-pages.py

ATTENTION : il ÉCRASE les six fichiers HTML. Si vous avez modifié le HTML
directement, reportez vos changements ici d'abord, ou supprimez ce dossier."""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAV = [
    ("index.html",      "Accueil"),
    ("services.html",   "Services"),
    ("pneus.html",      "Pneus"),
    ("occasions.html",  "Occasions"),
    ("nous.html",       "Le garage"),
    ("contact.html",    "Contact"),
]

ARROW  = '<svg viewBox="0 0 30 14" fill="none" aria-hidden="true"><path d="M1 7h27M22.5 1.5 28 7l-5.5 5.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_S= '<svg viewBox="0 0 26 14" fill="none" aria-hidden="true"><path d="M1 7h23M18.5 1.5 24 7l-5.5 5.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PHONE  = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6.5 3h3l1.5 4-2 1.4a12 12 0 0 0 6.6 6.6L17 13l4 1.5v3a2.5 2.5 0 0 1-2.7 2.5A16.8 16.8 0 0 1 3 5.7 2.5 2.5 0 0 1 5.5 3Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FB     = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M14.5 8.5V6.8c0-.8.3-1.3 1.4-1.3H17V2.6A18 18 0 0 0 14.9 2.5c-2.3 0-3.8 1.4-3.8 4v2h-2.6v3.2h2.6V21h3.4v-9.3h2.5l.4-3.2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
INFO   = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M12 11v5M12 7.8h.01" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>'
PIN    = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.6" stroke="currentColor" stroke-width="1.6"/></svg>'
CLOCK  = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v5.2l3.2 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
MAIL   = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2.5" stroke="currentColor" stroke-width="1.6"/><path d="m3.8 7 7.3 5.2a1.5 1.5 0 0 0 1.8 0L20.2 7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'

SCRIBBLE_A = ('<svg class="scribble" width="146" height="50" viewBox="0 0 146 50" fill="none" aria-hidden="true">'
              '<path d="M3 30C22 8 52 1 86 7c19 3 34 11 45 24"/>'
              '<path d="M117 21.5 132.5 31 123 43.5"/></svg>')
SCRIBBLE_B = ('<svg class="scribble" width="128" height="48" viewBox="0 0 128 48" fill="none" aria-hidden="true">'
              '<path d="M125 9C104 2 72 7 49 20 34 28 20 34 6 37"/>'
              '<path d="M19 29.5 5.5 37.5 16 45.5"/></svg>')

def nav_html(current, indent="        "):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ''
        out.append('%s<a href="%s"%s>%s</a>' % (indent, href, cur, label))
    return "\n".join(out)

def foot_links(current):
    return "\n".join(
        '            <li><a href="%s">%s</a></li>' % (h, l) for h, l in NAV if h != current
    )

JSONLD = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "AutoRepair",
    "name": "Garage Mecanochris",
    "description": "Garage indépendant à Sombreffe : entretien, réparation, diagnostic, freins, pneus et gardiennage de pneus, toutes marques.",
    "url": "https://mecanochris.be/",
    "telephone": "+3271885683",
    "email": "info@mecanochris.be",
    "vatID": "BE0500705090",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Chauss\u00e9e de Charleroi 185",
      "postalCode": "5140",
      "addressLocality": "Sombreffe",
      "addressRegion": "Namur",
      "addressCountry": "BE"
    },
    "openingHoursSpecification": [{
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "17:00"
    }],
    "sameAs": ["https://www.facebook.com/garagemecanochris"]
  }
  </script>'''

def page(slug, title, description, body, extra_head=""):
    head_nav = nav_html(slug)
    return '''<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>%(title)s</title>
  <meta name="description" content="%(description)s">
  <link rel="canonical" href="https://mecanochris.be/%(canon)s">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="fr_BE">
  <meta property="og:site_name" content="Garage Mecanochris">
  <meta property="og:title" content="%(title)s">
  <meta property="og:description" content="%(description)s">
  <meta property="og:image" content="https://mecanochris.be/assets/img/atelier-large.jpg">
  <meta name="theme-color" content="#E9E3D2">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="assets/fonts/abril-fatface-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/source-serif-4-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/style.css">
%(jsonld)s
%(extra)s
</head>
<body>
  <a class="skip" href="#contenu">Aller au contenu</a>

  <!-- ===== En-tête (identique sur les six pages) ===== -->
  <header class="site-head">
    <div class="wrap head-in">
      <a class="brand" href="index.html" aria-label="Garage Mecanochris, retour \u00e0 l\u2019accueil">
        <img src="assets/img/logo.png" width="1096" height="321" alt="Garage Mecanochris \u2014 m\u00e9canique toutes marques">
      </a>

      <nav class="nav" id="nav-principal" data-open="false" aria-label="Navigation principale">
%(nav)s
      </nav>

      <a class="tel-pill" href="tel:+3271885683">
        %(phone)s
        <span class="tel-text num">071 88 56 83</span>
        <span class="sr-only">Appeler le garage</span>
      </a>

      <button class="burger" type="button" aria-expanded="false" aria-controls="nav-principal">
        <span></span>
        <span class="sr-only">Ouvrir le menu</span>
      </button>
    </div>
  </header>

  <main id="contenu">
%(body)s
  </main>

  <!-- ===== Pied de page (identique sur les six pages) ===== -->
  <footer class="site-foot on-ink">
    <div class="wrap">
      <div class="foot-grid">
        <div>
          <img class="foot-logo" src="assets/img/logo.png" width="1096" height="321" alt="Garage Mecanochris">
          <p class="lede" style="margin-top:1.25rem;max-width:32ch">Un garage proche de vous, sur la chauss\u00e9e de Charleroi \u00e0 Sombreffe.</p>
        </div>

        <div class="foot-col">
          <h3>Atelier</h3>
          <ul>
            <li>Chauss\u00e9e de Charleroi 185</li>
            <li>5140 Sombreffe</li>
            <li style="color:var(--cream-dim)">\u00c0 c\u00f4t\u00e9 de la pompe Esso</li>
          </ul>
        </div>

        <div class="foot-col">
          <h3>Contact</h3>
          <ul>
            <li><a class="num" href="tel:+3271885683">071 88 56 83</a></li>
            <li><a href="mailto:info@mecanochris.be">info@mecanochris.be</a></li>
            <li style="color:var(--cream-dim)">Lun\u2013ven, 8 h \u2013 17 h</li>
          </ul>
        </div>

        <div class="foot-col">
          <h3>Le site</h3>
          <ul>
%(footlinks)s
          </ul>
        </div>
      </div>

      <div class="foot-bottom">
        <p>&copy; <span data-year>2026</span> Garage Mecanochris \u00b7 TVA BE 0500.705.090 \u00b7 Toute reproduction totale ou partielle de ce site est interdite sans autorisation expresse.</p>
        <div class="social">
          <a href="https://www.facebook.com/garagemecanochris" target="_blank" rel="noopener noreferrer" aria-label="Garage Mecanochris sur Facebook">%(fb)s</a>
        </div>
      </div>
    </div>
  </footer>

  <script src="assets/js/main.js" defer></script>
</body>
</html>
''' % {
    "title": title, "description": description,
    "canon": "" if slug == "index.html" else slug,
    "jsonld": JSONLD if slug == "index.html" else "",
    "extra": extra_head, "nav": head_nav, "phone": PHONE,
    "body": body, "footlinks": foot_links(slug), "fb": FB,
}

# =====================================================================
# Contenus
# =====================================================================

SERVICES = [
    ("entretien", "Entretien",
     "Du petit au gros entretien, toutes marques, dans le respect des préconisations du constructeur — et la préparation au contrôle technique.",
     "entretien.jpg", "Un mécanicien au travail sur un moteur dans l’atelier"),
    ("reparations", "Réparations",
     "Le savoir-faire de véritables spécialistes de l’automobile. Chaque prestation est effectuée dans le plus grand respect des recommandations des constructeurs.",
     "reparation.jpg", "Véhicule sur chandelles, outillage disposé au sol pendant une réparation"),
    ("diagnostic", "Diagnostic",
     "Nous analysons votre véhicule pour identifier la panne et cibler la réparation, plutôt que de remplacer au hasard.",
     "diag-laptop.jpg", "Mécanicien penché sur le compartiment moteur pendant un diagnostic"),
    ("freins", "Disques et plaquettes",
     "Remplacement des disques et plaquettes de freins, contrôle complet du circuit et de l’usure.",
     "freins.jpg", "Disque de frein et étrier démontés sur un établi"),
    ("pneus", "Pneus été / hiver",
     "Montage, équilibrage et permutation de vos pneus été comme hiver, au moment où la saison le demande.",
     "pneus.jpg", "Montage d’un pneu sur une jante en atelier"),
    ("gardiennage", "Gardiennage pneus",
     "Un très grand espace de stockage : nous gardons votre train de pneus hors saison, été comme hiver, toute l’année.",
     "gardiennage.jpg", "Piles de pneus étiquetés, rangés dans l’espace de stockage"),
]

def index_rows():
    out = []
    for slug, name, desc, img, alt in SERVICES:
        out.append('''          <li class="index-row">
            <a class="index-link" href="services.html#%s" data-preview="assets/img/%s">
              <span class="index-name">%s</span>
              <span class="index-desc">%s</span>
              <span class="index-go" aria-hidden="true">%s</span>
              <span class="index-thumb"><img src="assets/img/%s" width="600" height="338" alt="%s" loading="lazy" decoding="async"></span>
            </a>
          </li>''' % (slug, img, name, desc, ARROW_S, img, alt))
    return "\n".join(out)

CONTACT_PANEL = '''        <div class="panel panel-pad on-ink">
          <p class="label" style="margin:0 0 1.75rem">Nous trouver</p>
          <div class="contact-block">
            <div class="contact-line">
              <span class="label">Atelier</span>
              <strong>Chaussée de Charleroi 185<br>5140 Sombreffe</strong>
              <span style="color:var(--cream-dim)">À côté de la pompe Esso</span>
            </div>
            <hr class="rule">
            <div class="contact-line">
              <span class="label">Téléphone</span>
              <a class="num" href="tel:+3271885683">071 88 56 83</a>
            </div>
            <div class="contact-line">
              <span class="label">E-mail</span>
              <a href="mailto:info@mecanochris.be">info@mecanochris.be</a>
            </div>
            <hr class="rule">
            <div class="contact-line">
              <span class="label">Heures d’ouverture</span>
              <div style="margin-top:.4rem">
                <div class="hours-row"><span>Lundi – vendredi</span><span class="num">8 h – 17 h</span></div>
                <div class="hours-row" data-closed="true"><span>Samedi, dimanche, jours fériés</span><span>Fermé</span></div>
              </div>
              <p class="num" data-open-state style="margin-top:.9rem;font-weight:600;color:var(--rust)">Lun–ven, 8 h – 17 h</p>
            </div>
          </div>
        </div>'''

# ---------------------------------------------------------------- accueil
INDEX_BODY = '''    <section class="wrap hero">
      <div class="hero-title">
        <h1 class="display d-hero">
          <span class="rise"><span style="--i:0">Mécanique</span></span>
          <span class="rise"><span style="--i:1">toutes marques</span></span>
        </h1>
        <div class="hero-sub">
          <p class="lede">Entretien, réparation, diagnostic, freins et pneus. Un garage indépendant sur la chaussée de Charleroi à Sombreffe — juste à côté de la pompe Esso.</p>
          <a class="btn-line" href="services.html">Voir nos services %(arrow)s</a>
        </div>
      </div>

      <div class="panel hero-panel settle on-ink">
        <figure class="hero-figure">
          <img src="assets/img/atelier-large.jpg" width="1600" height="1067" alt="Intérieur de l’atelier : établis, outillage et rangements sous les néons" fetchpriority="high" decoding="async">
        </figure>
        <div class="hero-aside">
          <div>
            <span class="pill">L’atelier</span>
            <p class="hero-claim">Un service professionnel pour votre véhicule.</p>
          </div>
          <dl class="hero-facts">
            <div><dt>Adresse</dt><dd>Ch. de Charleroi 185, Sombreffe</dd></div>
            <div><dt>Téléphone</dt><dd><a class="num link" href="tel:+3271885683">071 88 56 83</a></dd></div>
            <div><dt>Ouverture</dt><dd class="txt-rust" data-open-state>Lun–ven, 8 h – 17 h</dd></div>
          </dl>
        </div>
      </div>

      <div class="hero-cta-row">
        <span class="bars" aria-hidden="true"><i></i><i></i></span>
        <a class="btn-blob" href="contact.html">Prendre rendez-vous %(arrow)s</a>
      </div>
    </section>

    <section class="band" aria-labelledby="t-services">
      <div class="wrap">
        <div class="split" style="align-items:end;margin-bottom:clamp(2rem,4vw,3.25rem)">
          <h2 class="display d-xl reveal" id="t-services">Ce que<br>nous faisons</h2>
          <p class="lede reveal">De la vidange au diagnostic électronique, six prestations qui couvrent l’essentiel de la vie d’une voiture — toutes marques, dans le respect des préconisations du constructeur.</p>
        </div>

        <ul class="index-list" data-preview-list>
%(rows)s
        </ul>

        <div class="hero-cta-row" style="margin-top:clamp(2rem,4vw,3rem);justify-content:flex-start;padding:0">
          <span class="bars" aria-hidden="true"><i></i><i></i></span>
          <a class="btn-line" href="services.html">Le détail des prestations %(arrow)s</a>
          %(scribbleB)s
        </div>
      </div>
    </section>

    <section class="band-tight" aria-labelledby="t-proximite">
      <div class="wrap proximity">
        <div>
          <h2 class="display d-xl reveal" id="t-proximite">Un service<br>de proximité</h2>
          <p class="lede" style="margin-top:1.5rem">Notre équipe est à votre service pour l’entretien comme pour la réparation de votre véhicule. Si vous avez la moindre question, nous sommes à votre écoute : nos spécialistes se feront un plaisir de vous recevoir au sein de notre garage.</p>
        </div>
%(contact)s
      </div>
    </section>

    <section class="band-tight" aria-labelledby="t-forts">
      <div class="wrap">
        <h2 class="sr-only" id="t-forts">Nos points forts</h2>
        <hr class="rule">
        <div class="cols-3" style="margin-top:clamp(2rem,4vw,3.25rem)">
          <div class="strength reveal">
            <h3>Efficacité</h3>
            <p>Un diagnostic qui cible la panne, plutôt qu’une liste de pièces remplacées au hasard.</p>
          </div>
          <div class="strength reveal">
            <h3>Rapidité</h3>
            <p>Un atelier à taille humaine : votre voiture ne fait pas la file derrière trente autres.</p>
          </div>
          <div class="strength reveal">
            <h3>Simplicité</h3>
            <p>Un coup de fil suffit. Nous vous disons ce qui est nécessaire et ce qui peut attendre.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="wrap band-tight">
      <div class="callout on-ink reveal">
        <div class="callout-in">
          <h2 class="display d-xl">Prenons soin de votre voiture.</h2>
          <a class="btn-blob" href="contact.html">Nous écrire %(arrow)s</a>
        </div>
      </div>
    </section>
''' % {"arrow": ARROW, "scribbleA": SCRIBBLE_A, "scribbleB": SCRIBBLE_B,
       "rows": index_rows(), "contact": CONTACT_PANEL}

# --------------------------------------------------------------- services
def service_sections():
    long_copy = {
        "entretien": "Vidange, filtres, courroies, bougies, contrôle des niveaux et des organes d’usure : nous réalisons le petit comme le gros entretien sur toutes les marques. Nous préparons également votre véhicule au contrôle technique, pour éviter le second passage.",
        "reparations": "Distribution, embrayage, suspension, échappement, circuit de refroidissement : la réparation est menée par de véritables spécialistes de l’automobile, dans le plus grand respect des recommandations du constructeur.",
        "diagnostic": "Un voyant s’allume, un bruit apparaît, la consommation grimpe. Nous branchons la valise, lisons les défauts et remplaçons ce qui doit l’être — le diagnostic sert à cibler la réparation, pas à rallonger la facture.",
        "freins": "Contrôle de l’usure, remplacement des disques et des plaquettes, vérification des étriers, des flexibles et du liquide. Le freinage est la première sécurité d’un véhicule : nous ne le laissons pas passer.",
        "pneus": "Montage, équilibrage et permutation de vos pneus été comme hiver. Vous avez déjà vos pneus ? Nous les posons. Vous n’en avez pas encore ? Nous vous conseillons la dimension et la gamme adaptées à votre véhicule.",
        "gardiennage": "Nous disposons d’un très grand espace de stockage. Vos pneus hors saison restent chez nous, protégés, et reviennent sur la voiture au bon moment — plus rien à rouler dans le garage à la maison.",
    }
    out = []
    for i, (slug, name, short, img, alt) in enumerate(SERVICES):
        flip = i % 2 == 1
        figure = ('        <figure class="figure-round ratio-4-5 reveal">\n'
                  '          <img src="assets/img/%s" width="1200" height="1500" alt="%s" loading="lazy" decoding="async" sizes="(max-width: 900px) 92vw, 44vw">\n'
                  '        </figure>' % (img, alt))
        text = ('        <div class="reveal" style="padding-block:clamp(0rem,2vw,2rem)">\n'
                '          <span class="pill pill-ink">%02d — Prestation</span>\n'
                '          <h2 class="display d-lg" style="margin:1.25rem 0 1rem">%s</h2>\n'
                '          <p class="lede" style="max-width:52ch">%s</p>\n'
                '          <p class="prose" style="margin-top:1.1rem;color:var(--muted)">%s</p>\n'
                '          <div class="hero-cta-row" style="margin-top:1.75rem;justify-content:flex-start;padding:0">\n'
                '            <span class="bars" aria-hidden="true"><i></i><i></i></span>\n'
                '            <a class="btn-line" href="contact.html">Demander un rendez-vous %s</a>\n'
                '          </div>\n'
                '        </div>' % (i + 1, name, short, long_copy[slug], ARROW))
        cols = (figure, text) if not flip else (text, figure)
        out.append('      <div class="split" id="%s" style="align-items:center;margin-top:clamp(2.5rem,6vw,5.5rem)">\n%s\n%s\n      </div>'
                   % (slug, cols[0], cols[1]))
    return "\n".join(out)

SERVICES_BODY = '''    <section class="wrap hero">
      <div class="hero-title">
        <h1 class="display d-hero">
          <span class="rise"><span style="--i:0">Nos services</span></span>
        </h1>
        <div class="hero-sub">
          <p class="lede">Six prestations, toutes marques, du petit entretien au diagnostic électronique. Chaque intervention est menée dans le respect des préconisations du constructeur.</p>
          <a class="btn-line" href="contact.html">Prendre rendez-vous %(arrow)s</a>
        </div>
      </div>
    </section>

    <section class="wrap" style="padding-bottom:clamp(3rem,7vw,6rem)">
%(sections)s
    </section>

    <section class="wrap band-tight">
      <div class="callout on-ink reveal">
        <div class="callout-in">
          <h2 class="display d-xl">Une panne, un doute, un bruit&nbsp;?</h2>
          <div style="display:grid;gap:1rem">
            <a class="btn-blob" href="tel:+3271885683">Appeler le 071 88 56 83</a>
            <p style="margin:0;color:var(--cream-dim);font-size:.95rem" class="num" data-open-state>Lun–ven, 8 h – 17 h</p>
          </div>
        </div>
      </div>
    </section>
''' % {"arrow": ARROW, "sections": service_sections()}

# ------------------------------------------------------------------ pneus
WIDTHS = [155, 165, 175, 185, 195, 205, 215, 225, 235, 245, 255]
HEIGHTS = [35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
DIAMS = [14, 15, 16, 17, 18, 19, 20, 21]

def opts(values, unit=""):
    return "".join('<option value="%s">%s%s</option>' % (v, v, unit) for v in values)

PNEUS_BODY = '''    <section class="wrap hero">
      <div class="hero-title">
        <h1 class="display d-hero">
          <span class="rise"><span style="--i:0">Pneus</span></span>
        </h1>
        <div class="hero-sub">
          <p class="lede">Montage, équilibrage, permutation et gardiennage. Donnez-nous la dimension inscrite sur le flanc de votre pneu, nous nous occupons du reste.</p>
          <a class="btn-line" href="tel:+3271885683">Appeler l’atelier %(arrow)s</a>
        </div>
      </div>

      <div class="panel panel-pad on-ink settle">
        <form class="tyre-search" data-tyre-form novalidate>
          <div>
            <span class="pill">Votre dimension</span>
            <p class="hero-claim" style="margin-top:1rem;max-width:28ch">Elle est gravée sur le flanc, par exemple <span class="num txt-rust">205/55 R16</span>.</p>
          </div>

          <div class="tyre-fields">
            <p class="field">
              <label class="label" for="largeur">Largeur</label>
              <select id="largeur" name="largeur">%(w)s</select>
            </p>
            <p class="field">
              <label class="label" for="hauteur">Hauteur</label>
              <select id="hauteur" name="hauteur">%(h)s</select>
            </p>
            <p class="field">
              <label class="label" for="diametre">Diamètre</label>
              <select id="diametre" name="diametre">%(d)s</select>
            </p>
            <p class="field">
              <label class="label" for="saison">Saison</label>
              <select id="saison" name="saison">
                <option value="été">Été</option>
                <option value="hiver">Hiver</option>
                <option value="4 saisons">4 saisons</option>
              </select>
            </p>
          </div>

          <div class="hero-cta-row" style="margin:0;padding:0;justify-content:flex-start">
            <button class="btn-blob" type="submit">Vérifier ma dimension %(arrow)s</button>
            <p class="tyre-note" style="margin:0">%(info)s Recherche de prix en direct via notre partenaire — pour l’instant, le devis se fait par téléphone.</p>
          </div>

          <p class="form-status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>

    <section class="band-tight">
      <div class="wrap split split-narrow" style="align-items:center">
        <figure class="figure-round ratio-4-5 reveal">
          <img src="assets/img/gardiennage.jpg" width="1400" height="1867" alt="Piles de pneus étiquetés, rangés dans l’espace de stockage" loading="lazy" decoding="async">
        </figure>
        <div class="reveal">
          <span class="pill pill-ink">Été / hiver</span>
          <h2 class="display d-xl" style="margin:1.25rem 0 1.25rem">Nous gardons vos pneus</h2>
          <p class="lede" style="max-width:50ch">Nous disposons d’un très grand espace de stockage, capable d’accueillir un grand nombre de pneus.</p>
          <p class="prose" style="margin-top:1.1rem;color:var(--muted);max-width:56ch">Votre train hors saison reste chez nous, à l’abri, et revient sur la voiture au moment du changement. Le gardiennage des pneus hiver est possible toute l’année — plus rien à stocker chez vous, plus rien à transporter dans le coffre.</p>
          <div class="hero-cta-row" style="margin-top:1.75rem;justify-content:flex-start;padding:0">
            <span class="bars" aria-hidden="true"><i></i><i></i></span>
            <a class="btn-line" href="contact.html">Réserver une place %(arrow)s</a>
            %(scribbleB)s
          </div>
        </div>
      </div>
    </section>

    <section class="band-tight">
      <div class="wrap">
        <hr class="rule">
        <div class="cols-3" style="margin-top:clamp(2rem,4vw,3.25rem)">
          <div class="strength reveal">
            <h3>Montage</h3>
            <p>Pose sur jante, valve neuve et équilibrage électronique, été comme hiver.</p>
          </div>
          <div class="strength reveal">
            <h3>Permutation</h3>
            <p>Avant / arrière au bon kilométrage, pour que les quatre pneus s’usent ensemble.</p>
          </div>
          <div class="strength reveal">
            <h3>Contrôle</h3>
            <p>Profondeur de sculpture, pression et usure irrégulière vérifiées à chaque passage.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="wrap band-tight">
      <div class="callout on-ink reveal">
        <div class="callout-in">
          <h2 class="display d-xl">Le bon pneu, posé le bon jour.</h2>
          <a class="btn-blob" href="contact.html">Demander un devis %(arrow)s</a>
        </div>
      </div>
    </section>
''' % {"arrow": ARROW, "info": INFO, "scribbleB": SCRIBBLE_B,
       "w": opts(WIDTHS), "h": opts(HEIGHTS), "d": opts(DIAMS, "″")}

# -------------------------------------------------------------- occasions
CARS = [
    ("occasion-1.jpg", "Volkswagen Golf 1.6 TDI", "12 900 €", "Berline compacte",
     [("Année", "2018"), ("Kilométrage", "96 000 km"), ("Carburant", "Diesel"),
      ("Boîte", "Manuelle"), ("Puissance", "115 ch"), ("Contrôle technique", "OK")],
     "Volkswagen Golf blanche photographiée de trois quarts avant"),
    ("occasion-2.jpg", "Renault Clio TCe 90", "11 450 €", "Citadine",
     [("Année", "2020"), ("Kilométrage", "54 300 km"), ("Carburant", "Essence"),
      ("Boîte", "Manuelle"), ("Puissance", "90 ch"), ("Contrôle technique", "OK")],
     "Renault Clio bleu foncé devant un mur orange"),
    ("occasion-3.jpg", "Audi A4 Avant 2.0 TDI", "15 900 €", "Break familial",
     [("Année", "2017"), ("Kilométrage", "148 000 km"), ("Carburant", "Diesel"),
      ("Boîte", "Automatique"), ("Puissance", "150 ch"), ("Contrôle technique", "OK")],
     "Break Audi gris photographié de trois quarts avant"),
]

def car_cards():
    out = []
    for img, name, price, kind, specs, alt in CARS:
        rows = "\n".join(
            '            <li><span>%s</span><span class="num">%s</span></li>' % (k, v) for k, v in specs)
        out.append('''        <article class="car reveal">
          <figure class="car-fig">
            <img src="assets/img/%s" width="1300" height="867" alt="%s" loading="lazy" decoding="async">
            <span class="car-tag">Exemple</span>
          </figure>
          <div class="car-head">
            <h2>%s</h2>
            <span class="car-price num">%s</span>
          </div>
          <p style="color:var(--muted);margin:.35rem 0 0">%s</p>
          <ul class="specs">
%s
          </ul>
        </article>''' % (img, alt, name, price, kind, rows))
    return "\n".join(out)

OCCASIONS_BODY = '''    <section class="wrap hero">
      <div class="hero-title">
        <h1 class="display d-hero">
          <span class="rise"><span style="--i:0">Occasions</span></span>
        </h1>
        <div class="hero-sub">
          <p class="lede">Des véhicules d’occasion préparés dans notre atelier : révisés, contrôlés, et suivis par ceux qui les ont remis en état.</p>
          <a class="btn-line" href="tel:+3271885683">Appeler l’atelier %(arrow)s</a>
        </div>
      </div>

      <div class="demo-note settle" role="note">
        %(info)s
        <p><strong>Exemples de présentation.</strong> Les trois véhicules ci-dessous sont des fiches de démonstration destinées à montrer la mise en page : les modèles, prix, kilométrages et photos ne correspondent à aucun véhicule réellement en stock. Ils sont à remplacer par le stock réel du garage avant la mise en ligne.</p>
      </div>
    </section>

    <section class="wrap" style="padding-bottom:clamp(3rem,7vw,6rem)">
      <div class="car-grid">
%(cards)s
      </div>
    </section>

    <section class="band-tight">
      <div class="wrap split" style="align-items:center">
        <div class="reveal">
          <h2 class="display d-xl">Préparée<br>dans l’atelier</h2>
          <p class="lede" style="margin-top:1.5rem;max-width:48ch">Une occasion qui sort d’ici est passée par les mêmes mains que les voitures que nous entretenons toute l’année.</p>
          <p class="prose" style="margin-top:1.1rem;color:var(--muted)">Entretien à jour, freinage contrôlé, pneus vérifiés, passage au contrôle technique préparé. Vous savez à qui vous vous adressez si quelque chose doit être revu — nous sommes à quinze minutes, pas dans une autre province.</p>
          <div class="hero-cta-row" style="margin-top:1.75rem;justify-content:flex-start;padding:0">
            <span class="bars" aria-hidden="true"><i></i><i></i></span>
            <a class="btn-line" href="contact.html">Une question sur un véhicule %(arrow)s</a>
          </div>
        </div>
        <figure class="figure-round ratio-3-2 reveal">
          <img src="assets/img/lift-blue.jpg" width="1400" height="933" alt="Véhicule ouvert en préparation dans l’atelier" loading="lazy" decoding="async">
        </figure>
      </div>
    </section>

    <section class="wrap band-tight">
      <div class="callout on-ink reveal">
        <div class="callout-in">
          <h2 class="display d-xl">Vous cherchez un modèle précis&nbsp;?</h2>
          <a class="btn-blob" href="contact.html">Dites-nous lequel %(arrow)s</a>
        </div>
      </div>
    </section>
''' % {"arrow": ARROW, "info": INFO, "cards": car_cards()}

# -------------------------------------------------------------------- nous
NOUS_BODY = '''    <section class="wrap hero">
      <div class="hero-title">
        <h1 class="display d-hero">
          <span class="rise"><span style="--i:0">Un garage</span></span>
          <span class="rise"><span style="--i:1">proche de vous</span></span>
        </h1>
        <div class="hero-sub">
          <p class="lede">Mecanochris est un atelier indépendant installé chaussée de Charleroi, à Sombreffe. Nous entretenons et réparons les véhicules de toutes les marques.</p>
          <a class="btn-line" href="contact.html">Venir nous voir %(arrow)s</a>
        </div>
      </div>

      <div class="panel settle on-ink" style="overflow:hidden">
        <figure style="margin:0;aspect-ratio:21/9">
          <img src="assets/img/atelier-large.jpg" width="1600" height="1067" alt="Vue large de l’atelier : établis, outillage et postes de travail" style="width:100%%;height:100%%;object-fit:cover;object-position:center 60%%" decoding="async">
        </figure>
      </div>
    </section>

    <section class="band-tight">
      <div class="wrap split split-wide" style="align-items:start">
        <div class="reveal">
          <span class="pill pill-ink">Le garage</span>
          <h2 class="display d-xl" style="margin:1.25rem 0 1.5rem">À votre écoute,<br>pas à la chaîne</h2>
          <div class="prose" style="color:var(--muted);max-width:56ch">
            <p>Notre équipe est à votre service afin de vous accompagner pour l’entretien ou la réparation de votre véhicule. Si vous avez la moindre question, nous sommes à votre écoute.</p>
            <p>Nos spécialistes se feront un plaisir de vous recevoir au sein de notre garage. Chaque prestation est effectuée dans le plus grand respect des recommandations des constructeurs, du petit entretien au gros travail de mécanique.</p>
            <p>Vous parlez directement à la personne qui travaille sur votre voiture. C’est ce qui change tout quand il faut expliquer un bruit, arbitrer une réparation ou décider de ce qui peut attendre.</p>
            <p><a class="link" href="https://www.facebook.com/garagemecanochris" target="_blank" rel="noopener noreferrer">Suivez l’atelier sur Facebook</a> pour les actualités et les photos des chantiers en cours.</p>
          </div>
        </div>
        <figure class="figure-round ratio-4-5 reveal">
          <img src="assets/img/portrait.jpg" width="1200" height="1800" alt="Mécanicien au travail sur un véhicule dans l’atelier" loading="lazy" decoding="async">
        </figure>
      </div>
    </section>

    <section class="band-tight">
      <div class="wrap">
        <hr class="rule">
        <div class="cols-3" style="margin-top:clamp(2rem,4vw,3.25rem)">
          <div class="strength reveal">
            <h3>Toutes marques</h3>
            <p>Aucune marque n’est écartée. La mécanique reste la mécanique, quel que soit le logo sur la calandre.</p>
          </div>
          <div class="strength reveal">
            <h3>Indépendant</h3>
            <p>Pas de quota à remplir ni de forfait imposé par une centrale : nous répondons devant vous, pas devant un réseau.</p>
          </div>
          <div class="strength reveal">
            <h3>À Sombreffe</h3>
            <p>Chaussée de Charleroi 185, à côté de la pompe Esso. Vous déposez la voiture et vous rentrez à pied.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="band-tight">
      <div class="wrap split" style="align-items:center">
        <figure class="figure-round ratio-3-2 reveal">
          <img src="assets/img/equipe.jpg" width="1400" height="905" alt="Mécanicien travaillant à l’établi dans l’atelier" loading="lazy" decoding="async">
        </figure>
%(contact)s
      </div>
    </section>

    <section class="wrap band-tight">
      <div class="callout on-ink reveal">
        <div class="callout-in">
          <h2 class="display d-xl">Passez quand vous voulez.</h2>
          <a class="btn-blob" href="contact.html">Nous contacter %(arrow)s</a>
        </div>
      </div>
    </section>
''' % {"arrow": ARROW, "contact": CONTACT_PANEL}

# ----------------------------------------------------------------- contact
CONTACT_BODY = '''    <section class="wrap hero">
      <div class="hero-title">
        <h1 class="display d-hero">
          <span class="rise"><span style="--i:0">Contactez-nous</span></span>
        </h1>
        <div class="hero-sub">
          <p class="lede">Un rendez-vous, un devis, une question sur une réparation : écrivez-nous, ou appelez directement l’atelier pendant les heures d’ouverture.</p>
          <a class="btn-line" href="tel:+3271885683">071 88 56 83 %(arrow)s</a>
        </div>
      </div>
    </section>

    <section class="wrap" style="padding-bottom:clamp(3rem,7vw,6rem)">
      <div class="split split-wide" style="align-items:start;gap:clamp(2rem,4vw,4rem)">

        <form class="form-paper" data-contact-form action="https://api.web3forms.com/submit" method="post" novalidate>
          <input type="hidden" name="access_key" value="VOTRE_CLE_WEB3FORMS">
          <input type="hidden" name="subject" value="Nouvelle demande depuis mecanochris.be">
          <input type="hidden" name="from_name" value="Site Garage Mecanochris">
          <input type="checkbox" name="botcheck" class="sr-only" tabindex="-1" autocomplete="off" aria-hidden="true">

          <span class="pill pill-ink">Demande d’informations</span>
          <h2 class="display d-lg" style="margin:1.25rem 0 1.75rem">Écrivez-nous</h2>

          <div class="form-grid">
            <p class="field">
              <label class="label" for="nom">Nom <span class="req" aria-hidden="true">*</span></label>
              <input id="nom" name="nom" type="text" required minlength="2" autocomplete="name" placeholder="Votre nom">
              <span class="field-error" aria-live="polite"></span>
            </p>
            <p class="field">
              <label class="label" for="tel">Téléphone <span class="req" aria-hidden="true">*</span></label>
              <input id="tel" name="telephone" type="tel" required autocomplete="tel" placeholder="0471 00 00 00">
              <span class="field-error" aria-live="polite"></span>
            </p>
            <p class="field field-full">
              <label class="label" for="email">E-mail <span class="req" aria-hidden="true">*</span></label>
              <input id="email" name="email" type="email" required autocomplete="email" placeholder="vous@exemple.be">
              <span class="field-error" aria-live="polite"></span>
            </p>
            <p class="field field-full">
              <label class="label" for="sujet">Sujet <span class="req" aria-hidden="true">*</span></label>
              <select id="sujet" name="sujet" required>
                <option value="Entretien">Entretien</option>
                <option value="Réparation">Réparation</option>
                <option value="Diagnostic">Diagnostic</option>
                <option value="Freins">Disques et plaquettes</option>
                <option value="Pneus">Pneus</option>
                <option value="Gardiennage pneus">Gardiennage pneus</option>
                <option value="Occasions">Véhicules d’occasion</option>
                <option value="Autre">Autre</option>
              </select>
              <span class="field-error" aria-live="polite"></span>
            </p>
            <p class="field field-full">
              <label class="label" for="message">Message <span class="req" aria-hidden="true">*</span></label>
              <textarea id="message" name="message" required minlength="10" placeholder="Marque, modèle, année, et ce que vous constatez."></textarea>
              <span class="field-error" aria-live="polite"></span>
            </p>
          </div>

          <p class="form-status" role="status" aria-live="polite"></p>

          <div class="hero-cta-row" style="margin-top:1.5rem;justify-content:flex-start;padding:0">
            <button class="btn-blob" type="submit">Envoyer la demande %(arrow)s</button>
            <p class="tyre-note" style="margin:0;color:var(--muted)">%(info)s <span>Les champs marqués d’une <span class="req">*</span> sont nécessaires pour vous répondre.</span></p>
          </div>
        </form>

%(contact)s
      </div>
    </section>

    <section class="band-tight">
      <div class="wrap">
        <hr class="rule">
        <div class="cols-3" style="margin-top:clamp(2rem,4vw,3.25rem)">
          <div class="strength reveal">
            <h3>Où&nbsp;?</h3>
            <p>Chaussée de Charleroi 185, 5140 Sombreffe. Le repère le plus simple&nbsp;: la pompe Esso — nous sommes juste à côté.</p>
            <p style="margin-top:1rem"><a class="link" href="https://www.google.com/maps/search/?api=1&amp;query=Chauss%%C3%%A9e+de+Charleroi+185%%2C+5140+Sombreffe" target="_blank" rel="noopener noreferrer">Ouvrir dans Maps</a></p>
          </div>
          <div class="strength reveal">
            <h3>Quand&nbsp;?</h3>
            <p>Du lundi au vendredi, de 8 h à 17 h. Fermé le samedi, le dimanche et les jours fériés.</p>
            <p class="num txt-rust" data-open-state style="margin-top:1rem;font-weight:600">Lun–ven, 8 h – 17 h</p>
          </div>
          <div class="strength reveal">
            <h3>Le garage</h3>
            <p>Garage Mecanochris — mécanique toutes marques.</p>
            <p class="num" style="margin-top:1rem">N° d’entreprise&nbsp;: BE 0500.705.090</p>
          </div>
        </div>
      </div>
    </section>
''' % {"arrow": ARROW, "info": INFO, "contact": CONTACT_PANEL}

# =====================================================================
PAGES = [
    ("index.html", "Garage Mecanochris — Mécanique toutes marques à Sombreffe",
     "Garage indépendant à Sombreffe : entretien, réparation, diagnostic, freins, pneus et gardiennage. Chaussée de Charleroi 185, à côté de la pompe Esso. 071 88 56 83.",
     INDEX_BODY),
    ("services.html", "Nos services — Garage Mecanochris, Sombreffe",
     "Entretien, réparations, diagnostic, disques et plaquettes, pneus été/hiver et gardiennage de pneus. Toutes marques, à Sombreffe.",
     SERVICES_BODY),
    ("pneus.html", "Pneus été et hiver, montage et gardiennage — Garage Mecanochris",
     "Montage, équilibrage, permutation et gardiennage de vos pneus été et hiver à Sombreffe. Un très grand espace de stockage à votre disposition.",
     PNEUS_BODY),
    ("occasions.html", "Véhicules d’occasion — Garage Mecanochris, Sombreffe",
     "Véhicules d’occasion préparés dans notre atelier de Sombreffe : révisés, contrôlés et suivis par ceux qui les ont remis en état.",
     OCCASIONS_BODY),
    ("nous.html", "Le garage — Garage Mecanochris, Sombreffe",
     "Un garage indépendant proche de vous, chaussée de Charleroi à Sombreffe. Toutes marques, à votre écoute, du petit entretien à la grosse mécanique.",
     NOUS_BODY),
    ("contact.html", "Contact et heures d’ouverture — Garage Mecanochris",
     "Contactez le Garage Mecanochris à Sombreffe : 071 88 56 83, info@mecanochris.be, chaussée de Charleroi 185. Ouvert du lundi au vendredi de 8 h à 17 h.",
     CONTACT_BODY),
]

for slug, title, desc, body in PAGES:
    html = page(slug, title, desc, body)
    with io.open(os.path.join(ROOT, slug), "w", encoding="utf-8") as fh:
        fh.write(html)
    print("%-16s %6d octets" % (slug, len(html.encode("utf-8"))))
