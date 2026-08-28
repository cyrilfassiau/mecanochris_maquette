# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Pure static: plain HTML, CSS and vanilla JS, no build step and no npm. Files open directly in a browser and deploy by upload to any static host (Netlify, Vercel, or classic FTP). Confirmed by the user; chosen so the site stays editable by hand after handover.

## Users

Private car owners in and around Sombreffe (Namur province, Wallonia, Belgium) — commuters, families and local workers who need a nearby independent garage for servicing, brakes, tires and breakdown diagnosis. They arrive on a phone, often after a search like "garage Sombreffe" or a Facebook link, and are doing one of four jobs: deciding whether this garage is competent and close enough, finding out what it can handle, checking opening hours or the address, or getting in touch to book a slot. A secondary audience is seasonal tire customers, who return twice a year for the summer/winter changeover and tire storage.

## Product Purpose

Garage Mecanochris is an independent, general-purpose car repair and servicing shop. The website exists to convert a local search into a phone call, a message or a visit: establish competence and proximity fast, state plainly what the garage does, and make the address, hours and contact details impossible to miss. Success is a booked job, not a session length.

## Positioning

A neighbourhood garage — "un service de proximité". Independent rather than a dealership chain: it services every make ("la réparation des véhicules de toutes les marques"), works to manufacturer recommendations, and its stated strengths are efficacité, rapidité, simplicité. The one capability a neighbouring garage could not simply claim is the large on-site tire storage facility, which keeps a customer's off-season set for them year-round.

## Operating Context

Walk-in and phone-first. Customers call 071 88 56 83 or come to the workshop; the site supports that rather than replacing it. Trade is weekday-only, which shapes expectations: anyone landing on a Saturday needs to know the garage is closed before they drive over. Tire work is strongly seasonal, peaking at the two changeover periods. The garage keeps an active Facebook page that in practice carries its news and photos.

## Capabilities and Constraints

Confirmed services:
- Entretiens — servicing from minor to major, all makes, plus "préparation contrôle technique" (Belgian roadworthiness-test prep).
- Réparations — repairs performed to manufacturer recommendations.
- Diagnostic — electronic vehicle diagnosis to locate a fault and scope the repair.
- Disques et plaquettes de freins — brake discs and pads replacement.
- Pneus — summer/winter tire fitting.
- Gardiennage pneus été/hiver — seasonal tire storage in a large on-site facility, available all year.

Site scope confirmed with the user: six pages — Accueil, Services, Nous, Informations (contact), Pneus, Occasions.

- Language: French only. No language switcher.
- Contact form: posts to a third-party form service (Formspree/Web3Forms class) delivering to info@mecanochris.be. The endpoint key is supplied by the user at the end; until then the form is wired but points at a documented placeholder.
- Pneus: the garage still uses the third-party Tiresleader/Centrale Pneus partner service. The new page presents a tire-search frontend as presentation only — no live search, no partner API integration.
- Occasions: the garage's used-vehicle page. There is no real inventory feed and no supplied listings. The user asked for 2–3 clearly-marked demo vehicles so the page shows its eventual shape. These are placeholders, must be labelled as such in the source, and must never be presented as real stock.
- Undecided / not supplied: real vehicle inventory, prices or rates, team size and names, certifications, photography of the workshop.

## Brand Commitments

- Name: Garage Mecanochris. Domain mecanochris.be.
- Existing tagline: "Un service professionnel pour votre véhicule."
- Recurring existing lines worth keeping: "Un garage proche de vous.", "Un service de proximité", "La meilleure solution pour votre voiture."
- Voice: plain, direct, reassuring, vouvoiement ("Nous vous proposons…", "N'hésitez pas à nous contacter"). Not jargon-heavy, not salesy.
- Facebook: https://www.facebook.com/garagemecanochris
- The user pinned a visual reference (an editorial, warm-cream and near-black classic-car layout with a heavy display serif and an orange accent) as binding for palette and design language.

## Evidence on Hand

Real, verified facts from the existing site — safe to publish:
- Address: Chaussée de Charleroi 185, 5140 Sombreffe — "à côté de la pompe Esso".
- Phone: 071 88 56 83.
- Email: info@mecanochris.be.
- Belgian company number (N° entreprise): 0500.705.090.
- Opening hours: Monday to Friday, 08:00–17:00. Closed Saturday, Sunday and public holidays.
- The six service descriptions listed above, in the garage's own words.
- The three stated strengths: Efficacité, Rapidité, Simplicité.

Absent — must not be fabricated: customer testimonials or reviews, star ratings, prices or hourly rates, years in business, number of cars serviced, staff names or headcount, certifications, brand approvals, warranty terms, used-car stock. Photography of the actual garage, workshop and team is not available; the only existing image assets are the logo and a single portrait, both low resolution.

## Product Principles

1. **The phone number and the address are the product.** Every page keeps calling, mapping and opening hours one gesture away; a visitor must never have to hunt for how to reach the garage.
2. **Claim only what the garage actually does.** Six real services, three real strengths, real hours. No invented reviews, counts, prices or credentials — an empty spot is better than a fabricated one.
3. **Phone-first, weekday-real.** Design for a thumb on a phone at the roadside, and make "closed weekends" visible before someone drives over.
4. **Proximity over polish-as-distance.** The site should read as a specific local workshop on the Chaussée de Charleroi, not as an anonymous national chain.
5. **Handover-safe.** Static, dependency-free and legible, so the garage's own contact details, hours and services can be edited later without a toolchain.

## Accessibility & Inclusion

No standard was contractually established. Treat WCAG 2.2 AA as the working floor, with particular weight on the two things this audience actually needs: readable type at arm's length on a phone in daylight, and tap targets that work with gloved or oily hands. All content in French, with `lang="fr"` set correctly.
