# Design

<!-- impeccable:design-schema 1 -->

## World

**L'atelier, mis en page comme une revue.** A working garage, laid out with the confidence of a printed motoring journal. Warm bone paper, blue-black ink, one rust-orange that only ever appears as a filled shape. Photography lives inside deep, heavily-rounded ink-black panels dropped onto the paper — the page is the paper, the panels are the windows into the workshop.

Pinned by the user's reference image (an editorial classic-car layout) and bound by their instruction: same colours, same design language. The reference's *subject* is not inherited — the character reads as craftsmanship and trust, never as a collector-car dealership. Modern cars, real tools, a real weekday workshop.

## Palette

Strategy: **Committed** — the bone paper owns the surface, ink panels own roughly a third, rust is the single voice that raises.

| Token | Value | Role |
|---|---|---|
| `--paper` | `#E9E3D2` | Warm bone ground. The page. |
| `--paper-deep` | `#DED7C3` | Alternate band, input wells, hairlines' backing. |
| `--ink` | `#191A24` | Blue-black. Panels, footer, body text on paper. |
| `--ink-soft` | `#23242F` | Raised surfaces inside a panel. |
| `--cream` | `#EFEADB` | Text on ink. 14.4:1. |
| `--cream-dim` | `#A9A091` | Secondary text on ink, tinted warm, never grey. 6.7:1. |
| `--muted` | `#625B4B` | Secondary text on paper. 5.3:1. |
| `--rust` | `#DD6420` | **Fills and large display only.** 2.8:1 on paper — never body text there. 4.9:1 on ink, so it may be text on a panel. |
| `--rust-ink` | `#9E4110` | The text-safe rust. Links and small labels on paper. 5.1:1. |
| `--rust-deep` | `#B94F14` | Reserved. Not used for a surface carrying text. |
| `--rust-lift` | `#EE7628` | Hover state of a rust fill. Hover **lightens**; darkening drops ink below 4.5:1. |

Two rules keep this palette honest:

1. **The rust split.** The bright rust is a *material*, the dark rust is *language*. `--rust` fills shapes; `--rust-ink` writes words on paper.
2. **Ink on rust, never cream.** Cream on `--rust` is 2.95:1 and fails. Ink on `--rust` is 4.87:1 and reads better anyway — a near-black word on a grainy orange pill is the print register this world is borrowing from. Every rust surface that carries a label, an icon, or a caret uses ink: the primary button, the outline button on hover, the phone pill on hover, the social icon on hover, and the text selection.

## Type

Self-hosted, no CDN — a Belgian site should not hand visitor IPs to Google Fonts.

- **Display — Abril Fatface.** Fat didone, ball terminals, high contrast. The reference's lettering as an object. Used only at size, tracking `-0.03em`, never below 1.5rem.
- **Text — Source Serif 4** (variable 300–700, roman + italic). Body, navigation, labels, forms. An all-serif page, as the reference is.

Hero display runs to `clamp(3.2rem, 12vw, 9.5rem)` — a deliberate step past the usual 6rem ceiling, because the pinned reference's entire impact is viewport-scale lettering. Every other display size stays at or under 6rem. Body measure holds 62–72ch.

## Materials

- **Paper grain.** An `feTurbulence` fractal-noise SVG, encoded inline, multiplied over the whole page at low opacity, and again at higher strength inside every rust fill. This is the single material that makes the palette read as printed rather than flat.
- **Ink panels.** `border-radius: 40px` (28px under 700px), no border, no shadow on paper — they sit *in* the page, not above it.
- **Depth.** Where a shadow is used (the sticky header once scrolled, the floating service preview), it carries a real offset and a soft blur tinted with the ink hue. No zero-offset halos.
- **The rust blob.** A large, grainy, pill-shaped rust button with a thin arrow, allowed to overlap the edge of the panel it belongs to. The reference's most distinctive object.
- **The double-bar.** Two short rounded rust bars set before a secondary call to action. A recurring punctuation mark, not decoration.
- **Drawn arrows.** Hand-drawn single-stroke rust squiggles, authored as SVG paths with round caps.

## Components

Outline pill button (`.btn-line`), rust blob button (`.btn-blob`), label pill (`.pill`), ink panel (`.panel`), service index row, spec table, form field with rust caret and focus ring, footer.

Icons are authored SVG on one 1.6px stroke, round cap and join. No emoji, no unicode glyphs.

## Motion

One authored moment: on load the hero lettering rises line by line under a `clip-path` wipe while the first ink panel settles from `scale(.965)` with a lifting blur — exponential ease-out, ~900ms, staggered 70ms. Nothing else on the page repeats that entrance.

The signature interaction is the **service index**: hovering a row lifts its row weight and floats that service's photograph beside the cursor, tracked with a lerp so it trails rather than snaps. Below 900px the images sit inline and no tracking runs.

Everything respects `prefers-reduced-motion: reduce`, which removes transforms and reveals content in place.

## Browser surfaces

Themed from the palette, not left to the browser: selection (rust on cream), caret, focus ring (2px rust-ink offset 3px), scrollbar (paper track, ink thumb), underline offset and thickness on prose links, and `font-variant-numeric: tabular-nums` on every table of specs, prices and phone numbers.
