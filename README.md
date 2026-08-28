# Garage Mecanochris — site statique

Refonte du site de https://mecanochris.be. HTML, CSS et JavaScript purs : **aucune étape de build, aucune dépendance npm**. Ouvrez `index.html` dans un navigateur, ça fonctionne.

---

## 1. Prévisualiser

Un double-clic sur `index.html` suffit pour l'essentiel. Pour que tout se comporte exactement comme en ligne, servez le dossier :

```bash
python3 -m http.server 4321
```

Puis ouvrez http://localhost:4321.

## 2. Mettre en ligne

Déposez le contenu du dossier tel quel : Netlify, Vercel, Cloudflare Pages, ou un simple FTP chez l'hébergeur actuel. Il n'y a rien à compiler.

---

## 3. À FAIRE avant la mise en ligne

### 3.1 Connecter le formulaire de contact (5 minutes, obligatoire)

Le formulaire est câblé mais pas encore relié. Tant que ce n'est pas fait, il affiche un message qui renvoie vers le téléphone.

1. Créez un compte gratuit sur https://web3forms.com (aucune carte demandée).
2. Indiquez `info@mecanochris.be` comme adresse de réception. Vous recevez une clé d'accès par e-mail.
3. Ouvrez `contact.html`, cherchez la ligne :

   ```html
   <input type="hidden" name="access_key" value="VOTRE_CLE_WEB3FORMS">
   ```

4. Remplacez `VOTRE_CLE_WEB3FORMS` par la clé reçue. C'est tout.

Un piège à robots (`botcheck`) est déjà en place. Rien d'autre à configurer.

### 3.2 Remplacer les photos

**Toutes les photos actuelles sont des photos libres de droits (Unsplash, usage commercial autorisé, sans attribution obligatoire).** Elles tiennent la mise en page mais ne montrent pas le vrai garage. Voici exactement quoi photographier pour chacune. Gardez le **même nom de fichier** et le site se met à jour tout seul.

| Fichier | Où il apparaît | Format | À photographier |
|---|---|---|---|
| `atelier-large.jpg` | Accueil (grand panneau) + bandeau « Le garage » | paysage, ≥ 1600 px de large | **La photo la plus importante du site.** Vue large de l'atelier depuis l'entrée : ponts, établis, outillage. De jour, lumières allumées. |
| `entretien.jpg` | Services → Entretien | portrait, ≥ 1200 px | Un mécanicien en train de travailler sur un véhicule, vu de près. |
| `reparation.jpg` | Services → Réparations | portrait, ≥ 1200 px | Une réparation en cours : voiture sur pont ou sur chandelles, outils en main. |
| `diag-laptop.jpg` | Services → Diagnostic | portrait, ≥ 1200 px | La valise de diagnostic branchée, écran visible. |
| `freins.jpg` | Services → Disques et plaquettes | portrait, ≥ 1200 px | Un disque et des plaquettes démontés, roue déposée. |
| `pneus.jpg` | Services → Pneus | portrait, ≥ 1200 px | Montage ou équilibrage d'un pneu sur la machine. |
| `gardiennage.jpg` | Services + page Pneus | portrait, ≥ 1200 px | **Votre espace de stockage réel.** C'est votre argument le plus distinctif : montrez le volume et les pneus étiquetés. |
| `portrait.jpg` | Le garage | portrait, ≥ 1000 px | Christopher (ou l'équipe) au travail, pas en pose. |
| `equipe.jpg` | Le garage | paysage, ≥ 1200 px | Un second plan de travail : établi, machine, geste précis. |
| `lift-blue.jpg` | Occasions | paysage, ≥ 1200 px | Un véhicule en préparation dans l'atelier. |
| `occasion-1/2/3.jpg` | Occasions | paysage 3/2, ≥ 1200 px | Les vrais véhicules en stock (voir 3.3). |

Conseils de prise de vue : téléphone récent en mode paysage, portes de l'atelier ouvertes pour la lumière, sol dégagé au premier plan. Exportez en JPEG de qualité ~80 % et visez moins de 400 Ko par image.

Le logo (`assets/img/logo.png`) a été détouré depuis l'ancien site : le fond gris a été retiré, il est maintenant en noir sur fond transparent et s'inverse proprement en crème dans le pied de page.

### 3.3 Remplacer les véhicules d'occasion

`occasions.html` contient **trois fiches de démonstration**, signalées comme telles à l'écran par un encadré et par une étiquette « Exemple » sur chaque photo. Les modèles, prix et kilométrages sont inventés et ne correspondent à aucun véhicule réel.

Avant la mise en ligne, soit vous remplacez ces trois fiches par le stock réel, soit vous supprimez la page (et son lien dans le menu, présent dans les six fichiers HTML). **Ne publiez pas les fiches de démonstration telles quelles.**

Pour modifier une fiche, cherchez `<article class="car reveal">` dans `occasions.html` : le nom, le prix et les six caractéristiques sont en clair, l'un sous l'autre.

---

## 4. Ce qui a été repris de l'ancien site

Toutes les informations factuelles proviennent de mecanochris.be et n'ont pas été modifiées :

- Chaussée de Charleroi 185, 5140 Sombreffe — à côté de la pompe Esso
- 071 88 56 83 · info@mecanochris.be · N° d'entreprise BE 0500.705.090
- Du lundi au vendredi, 8 h – 17 h. Fermé samedi, dimanche et jours fériés.
- Les six prestations, décrites dans les mots du garage
- Les trois points forts : Efficacité, Rapidité, Simplicité
- La page Facebook

**Rien n'a été inventé** : pas d'avis clients, pas de note, pas de tarif, pas d'ancienneté, pas de certification. Ces éléments sont absents volontairement — ajoutez-les seulement quand ils seront réels.

## 5. La page Pneus

Le formulaire de dimension est **une présentation** : il affiche un récapitulatif et renvoie vers le téléphone. La recherche de prix en direct passe toujours par votre partenaire Tiresleader, qui n'est pas connecté ici. Le jour où vous voudrez le brancher, tout est prêt dans `assets/js/main.js` (bloc `tyreDemo`).

## 6. Structure

```
index.html · services.html · pneus.html · occasions.html · nous.html · contact.html
assets/
  css/style.css     tout le style, un seul fichier commenté
  js/main.js        menu, animations, formulaire, horaires en direct
  img/              photos, logo, favicon
  fonts/            Abril Fatface + Source Serif 4 (auto-hébergées)
outils/
  generer-pages.py  optionnel — voir ci-dessous
README.md · PRODUCT.md · DESIGN.md
```

**L'en-tête et le pied de page sont recopiés à l'identique dans les six fichiers** (c'est la contrepartie d'un site sans build : le HTML est complet, donc lisible par Google et par n'importe quel hébergeur). Si vous modifiez le menu, faites-le dans les six fichiers.

`outils/generer-pages.py` régénère les six pages depuis un gabarit unique, ce qui évite cette recopie manuelle :

```bash
python3 outils/generer-pages.py
```

Il est **facultatif** — les fichiers HTML livrés fonctionnent sans lui. Si vous préférez éditer le HTML à la main, ignorez ce dossier (et supprimez-le, pour éviter qu'une exécution ultérieure n'écrase vos modifications).

## 7. Notes techniques

- **Polices auto-hébergées.** Elles ne passent pas par le CDN Google : en Belgique, appeler Google Fonts depuis le navigateur du visiteur transmet son adresse IP à Google, ce qui pose un problème RGPD. Les fichiers sont dans `assets/fonts/`.
- **Horaires en direct.** Le site calcule « Ouvert maintenant » / « Fermé » sur le fuseau Europe/Brussels, d'après les horaires réels. Pour les modifier, cherchez `openState` dans `assets/js/main.js`.
- **Accessibilité.** Contrastes vérifiés (tous ≥ 4,5:1), navigation au clavier, focus visibles, `prefers-reduced-motion` respecté, formulaire avec messages d'erreur explicites en français.
- **Référencement local.** Données structurées `AutoRepair` (adresse, téléphone, horaires, TVA) dans `index.html`, titres et descriptions rédigés page par page autour de « garage Sombreffe ».
- **Poids.** ~480 Ko au premier affichage de l'accueil, dont 238 Ko pour la photo de l'atelier. Compressez vos propres photos avant de les déposer.
