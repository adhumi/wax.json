# Spécifications Fonctionnelles — Glide Wax

**Version :** 1.0  
**Date :** 26 février 2026  
**Plateforme :** iOS (iPhone) — App standalone  
**Langues :** Français, Anglais (V1)  
**Nom affiché :** Glide Wax  
**Identifiant technique :** GlideWax

---

## 1. Vision produit

**Glide Wax** est une application iOS d'aide à la décision pour le fartage de glisse en ski de fond. L'app recommande le meilleur fart (ou combinaison multicouche) en croisant les conditions météo, le type de neige, le profil de l'utilisateur et son stock de farts disponibles. Lorsque Apple Intelligence est disponible sur l'appareil, le moteur de recommandation est enrichi par le LLM embarqué pour affiner le scoring et fournir un commentaire contextuel en langage naturel.

---

## 2. Base de données farts

### 2.1 Source

Fichier JSON embarqué `glide_wax.json` — 191 produits, 22 marques. Maintenu dans un repo Git dédié (https://github.com/adhumi/wax.json) et intégré au projet via **submodule Git**. Validé par JSON Schema (`glide_wax_schema.json`, même repo). Mis à jour annuellement (cycle septembre–novembre, publication des nouvelles gammes fabricants). La mise à jour du catalogue dans l'app se fait via `git submodule update --remote wax.json`.

### 2.2 Internationalisation du catalogue

Le JSON suit un pattern `LocalizedString` défini dans le schéma pour les champs textuels destinés à l'affichage :

```json
"comment": {
    "fr_FR": "Pour le froid extrême. Remplace CH4X.",
    "en_US": "For extreme cold. Replaces CH4X."
}
```

**Contraintes du schéma (`LocalizedString`) :**
- Les clés suivent le pattern locale `^[a-z]{2}_[A-Z]{2}$` (ex. `fr_FR`, `en_US`, `de_DE`)
- La clé `fr_FR` est **obligatoire** (seule locale garantie présente)
- Les valeurs peuvent être `string` ou `null` (traduction en attente)
- Extensible : ajouter une langue = ajouter une clé dans le JSON, sans changer le schéma

En V1, seul le champ `comment` est localisé (FR + EN). Les enums (`snow_type`, `level`, `format_type`, `role`) sont stockées en anglais dans le JSON et traduites côté app via des tables de correspondance statiques (voir §10.2).

### 2.3 Champs exploités par le moteur

| Champ JSON | Type | Usage moteur |
|---|---|---|
| `id` | String (slug) | Identifiant unique |
| `name` | String | Affichage |
| `brand` | String | Filtre marques préférées |
| `product_line` | String | Affichage / groupement |
| `format_type` | FormatType enum | Déterminer le mode d'application (fer, liquide…) |
| `temp_min_c`, `temp_max_c` | Int? | Matching température air |
| `iron_temp_c` | Int? | Protocole de fartage (null = pas de fer) |
| `snow_type` | [SnowType] | Matching type de neige |
| `humidity_min`, `humidity_max` | Int? | Matching humidité relative |
| `humidity_source` | HumiditySource? | Pondération confiance |
| `level` | Level enum | Filtre par profil |
| `role` | [Role] | Composition multicouche |
| `eco` | Bool | Filtre préférence éco |
| `fluorinated` | Bool | Filtre conformité (toujours false en v7) |
| `fis_compliant` | Bool | Filtre compétition FIS |
| `comment` | LocalizedString | Affichage (fr_FR, en_US) |
| `durability_km` | Int? | Info protocole longue distance |
| `active` | Bool | Exclure produits discontinués |
| `image_url` | String (URI) | Affichage visuel |
| `product_url` | String (URI) | Lien vers fiche fabricant |
| `date_added`, `date_updated` | String (date) | Maintenance |

### 2.4 Enums du schéma

**SnowType** (12 valeurs) :
`heavy_new`, `artificial`, `fresh_falling`, `fine_fresh`, `mixed_new_dirty_base`, `compact`, `compact_glazed`, `compact_dirty`, `transformed`, `wet`, `dry_grain`, `wet_grain`

**FormatType** (8 valeurs) :
`block_hot`, `block_rub_roto`, `block_rub`, `liquid`, `liquid_spray`, `powder_hot`, `powder`, `paste_rub`

**Level** : `beginner`, `sport`, `expert`

**Role** : `base_prep`, `base`, `day_wax`, `top_coat`, `universal`, `cleaner`, `additive`

**HumiditySource** : `manufacturer`, `color_inference`, `community`

### 2.5 Contraintes de validation (JSON Schema)

Le schéma (`glide_wax_schema.json`, `$id: https://arnuva.app/schemas/glide_wax_v7_2.schema.json`) impose des contraintes strictes validées en CI :

| Champ | Contrainte |
|---|---|
| `id` | Pattern `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$` (slug lowercase) |
| `temp_min_c` | `[-50, 10]` ou `null` |
| `temp_max_c` | `[-40, 25]` ou `null` |
| `iron_temp_c` | `[80, 200]` ou `null` (null = produit sans fer) |
| `humidity_min`, `humidity_max` | `[0, 100]` ou `null` |
| `durability_km` | `≥ 0` ou `null` |
| `snow_type` | Array de SnowType, `uniqueItems`. **Peut être vide** (base_prep, cleaners) |
| `role` | Array de Role, `minItems: 1`, `uniqueItems` |
| `image_url`, `product_url` | `format: "uri"` |
| `date_added`, `date_updated` | `format: "date"` (ISO 8601) |
| Product | `additionalProperties: false` — aucun champ non déclaré |
| Tous les champs | `required` — les champs nullable sont présents avec valeur `null`, jamais absents |

---

## 3. Architecture fonctionnelle

### 3.1 Flux principal

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────┐
│  Conditions  │───▶│   Filtrage   │───▶│   Scoring    │───▶│  Résultat   │
│  (entrées)   │    │  (2 pools)   │    │ + composition│    │  (podium    │
│              │    │  stock +     │    │ + bonus dispo│    │   mixte)    │
│              │    │  marques fav │    │              │    │             │
└─────────────┘    └──────────────┘    └──────────────┘    └─────────────┘
       │                                      │                    │
       ▼                                      ▼                    ▼
  WeatherKit +                         Apple Intelligence    Apple Intelligence
  saisie manuelle                      (scoring enrichi)     (commentaire NL)
```

### 3.2 Modules

- **ConditionsModule** — Collecte des entrées (météo, neige, profil)
- **InventoryModule** — Gestion du stock persistant
- **FilterEngine** — Réduction du catalogue selon contraintes
- **ScoringEngine** — Classement par compatibilité
- **LayerComposer** — Composition multicouche (mode expert)
- **ProtocolGenerator** — Génération du protocole de fartage
- **AIEnhancer** — Enrichissement Apple Intelligence (optionnel)

---

## 4. Entrées utilisateur

### 4.1 Conditions météo

**Source primaire : WeatherKit (automatique)**

L'app géolocalise l'utilisateur ou lui permet de sélectionner un lieu (station de ski, coordonnées GPS d'un parcours). WeatherKit fournit :
- Température air actuelle (°C)
- Humidité relative (%)
- Tendance météo (prochaines heures)

**Override manuel**

L'utilisateur peut corriger chaque valeur. Un champ libre permet de saisir la température neige si connue (thermomètre sur place). L'override est signalé visuellement (icône "manuel") et persiste jusqu'à reset.

**Logique de priorité :**  
Si override actif → utiliser la valeur manuelle.  
Sinon → valeur WeatherKit.  
Si WeatherKit indisponible (hors réseau) → saisie manuelle obligatoire.

### 4.2 Type de neige

Sélection directe parmi les 12 types du catalogue (`SnowType` enum). Les labels sont traduits côté app (voir §10.2) :

| Enum (JSON) | FR | EN |
|---|---|---|
| `fresh_falling` | Fraîche tombante | Fresh falling |
| `fine_fresh` | Fraîche fine | Fine fresh |
| `heavy_new` | Neuve lourde | Heavy new |
| `artificial` | Neige artificielle | Artificial |
| `mixed_new_dirty_base` | Mixte neuve sur fond sale | Mixed new on dirty base |
| `compact` | Compacte | Compact |
| `compact_glazed` | Compacte lustrée | Compact glazed |
| `compact_dirty` | Compacte sale | Compact dirty |
| `transformed` | Transformée | Transformed |
| `wet` | Mouillée | Wet |
| `dry_grain` | Petit à gros grain sec | Dry grain |
| `wet_grain` | Gros grain mouillé | Wet grain |

Chaque type est présenté avec une icône descriptive et une courte phrase d'aide localisée (ex. FR : "Compacte lustrée — Surface dure et brillante, typique après damage et passage répété"). Sélection multiple autorisée (ex. `compact` + `artificial`).

### 4.3 Profil utilisateur

Trois profils fixes déterminent le mode de recommandation :

| Profil (app) | Enum Swift | Couches | Filtrage `level` (JSON) | Résultat |
|---|---|---|---|---|
| **Loisir** | `.leisure` | 1 (mono-couche) | `beginner` uniquement | 1 fart recommandé |
| **Sportif** | `.sport` | 2 (base + day wax) | `beginner` + `sport` | Combo 2 couches |
| **Compétition** | `.competition` | 2-3 (base + day + top coat) | Tout (`beginner` + `sport` + `expert`) | Combo optimal |

Le profil app (`UserProfile`) détermine à la fois le nombre de couches et le sous-ensemble de produits visibles, filtré par le champ `level` du schéma. Un utilisateur "Loisir" ne voit que les produits `beginner` (universels, day wax simples), un "Compétition" accède à tout le catalogue y compris les produits `expert`.

**Mode libre (expert)** : accessible depuis n'importe quel profil via un toggle. L'utilisateur compose manuellement ses couches en choisissant le rôle de chaque slot (base_prep → base → day_wax → top_coat). Le moteur score chaque slot indépendamment et alerte si une combinaison est incohérente (ex. base froide + top coat chaud). En mode libre, aucun filtre `level` n'est appliqué.

Le profil est persisté dans les réglages et modifiable à tout moment.

### 4.4 Préférences persistantes (Réglages)

| Préférence | Type | Défaut |
|---|---|---|
| Marques autorisées | Multi-sélection (22 marques) | Toutes |
| Préférence éco | Bool | false |
| Conformité FIS | Bool | false |
| Profil | Enum (`leisure` / `sport` / `competition`) | `sport` |
| Unités température | °C / °F | °C |
| Langue | FR / EN | Langue système |

---

## 5. Inventaire (stock de farts)

### 5.1 Modèle de données

```
WaxInventoryItem {
    waxId: String           // Référence vers product.id
    dateAdded: Date
    status: StockStatus     // .new | .opened | .almostEmpty
    notes: String?          // Notes libres
}
```

### 5.2 Fonctionnalités

**Ajout au stock :**
- Recherche textuelle dans le catalogue (nom, marque)
- Filtrage par marque
- Scan (futur V2 : reconnaissance visuelle du produit)

**Gestion :**
- Modifier le statut (new → opened → almost empty)
- Supprimer du stock
- Notes libres par produit

**Interaction avec le moteur :**

Le moteur travaille systématiquement sur deux pools en parallèle et présente un résultat mixte :

- **Pool "Mon stock"** : candidats limités aux farts en inventaire. Produit les combinaisons réalisables immédiatement.
- **Pool "Marques favorites"** : candidats issus de toutes les marques autorisées dans les réglages (y compris les produits hors stock). Produit les combinaisons optimales théoriques.

Les deux pools sont scorés puis fusionnés dans un classement unique, avec un **bonus de disponibilité** pour les combinaisons 100% en stock (voir §6.2). L'utilisateur voit d'un coup d'œil ce qu'il peut faire tout de suite et ce qu'il pourrait faire en achetant un produit manquant.

### 5.3 Persistance

SwiftData, stockage local. Pas de synchronisation cloud en V1 (pas de backend).

---

## 6. Moteur de recommandation

### 6.1 Pipeline de filtrage (entonnoir double)

Le moteur exécute deux pipelines de filtrage en parallèle, produisant deux pools de candidats :

```
Catalogue (191 produits)
  │
  ├─ [1] active == true                          → exclure discontinués
  ├─ [2] level ∈ niveaux_autorisés(profil)       → filtre par profil utilisateur
  │        leisure → [beginner]
  │        sport   → [beginner, sport]
  │        competition → [beginner, sport, expert]
  │        mode libre → pas de filtre
  ├─ [3] Si pref_eco : eco == true               → filtre éco
  ├─ [4] Si pref_fis : fis_compliant == true      → conformité FIS
  ├─ [5] role ∩ roles_requis ≠ ∅                 → rôles selon profil
  │
  ├─── Pool A "Mon stock" ──────────────────────
  │     └─ [6a] id ∈ inventaire                   → stock uniquement
  │
  └─── Pool B "Marques favorites" ──────────────
        └─ [6b] brand ∈ marques_autorisees        → marques préférées
              (inclut aussi les produits en stock)
```

Les étapes [1] à [5] sont communes. Les pools divergent uniquement sur le critère de disponibilité (stock vs marques). Le Pool B est un sur-ensemble du Pool A.

### 6.2 Scoring algorithmique

Chaque produit candidat reçoit un score sur 100, composé de trois dimensions pondérées :

#### Score température (poids : 50%)

```
Si temp_min_c et temp_max_c non null :
    plage_produit = [temp_min_c, temp_max_c]
    temp_air = conditions.temperature

    Si temp_air ∈ plage_produit :
        // Position dans la plage : centré = meilleur
        centre = (temp_min_c + temp_max_c) / 2
        distance_centre = |temp_air - centre|
        demi_plage = (temp_max_c - temp_min_c) / 2
        score_temp = 100 - (distance_centre / demi_plage) × 30
    Si temp_air hors plage :
        ecart = min(|temp_air - temp_min_c|, |temp_air - temp_max_c|)
        score_temp = max(0, 70 - ecart × 10)

Sinon (universel, null) :
    score_temp = 60  // score neutre
```

#### Score humidité (poids : 30%)

```
Si humidity_min et humidity_max non null :
    humidite_air = conditions.humidity

    Si humidite_air ∈ [humidity_min, humidity_max] :
        score_hum = 100
    Sinon :
        ecart = distance au range
        score_hum = max(0, 80 - ecart × 2)

    // Pondération par fiabilité source
    Si humidity_source == "manufacturer" : poids_confiance = 1.0
    Si humidity_source == "color_inference" : poids_confiance = 0.7
    Si humidity_source == "community" : poids_confiance = 0.5

    score_hum = score_hum × poids_confiance

Sinon (null) :
    score_hum = 50  // neutre, pas de pénalité forte
```

#### Score neige (poids : 20%)

```
types_neige_user = conditions.snowTypes     // [SnowType]
types_neige_produit = product.snow_type     // [SnowType] — peut être vide (base_prep, cleaners)

Si types_neige_produit est vide :
    score_neige = 50  // neutre (produit non spécifique à un type de neige)
Sinon :
    intersection = types_neige_user ∩ types_neige_produit
    couverture = |intersection| / |types_neige_user|
    score_neige = couverture × 100
```

#### Score final

```
score_final = score_temp × 0.50
            + score_hum  × 0.30
            + score_neige × 0.20
```

#### Bonus / malus produit

| Condition | Ajustement |
|---|---|
| `durability_km` non null et sortie longue distance | +5 |
| Statut stock `almost_empty` | -3 (signalé mais pas éliminé) |

#### Bonus de disponibilité (appliqué sur le score combinaison)

Le bonus de disponibilité est le levier principal pour favoriser les combos réalisables immédiatement, tout en laissant remonter les combos optimales nécessitant un achat.

| Disponibilité de la combinaison | Bonus |
|---|---|
| **100% en stock** (tous les produits de la combo) | **+10** |
| **Partiellement en stock** (≥ 1 produit en stock) | +3 |
| **Rien en stock** (tout à acheter) | 0 |

Ce bonus est ajouté au `score_combo` (voir §6.3) après la moyenne pondérée des couches. Ainsi, une combinaison en stock à score technique 82 (→ 92) surclasse une combinaison à acheter à score 88 (→ 88), mais pas une à score 95 (→ 95). L'utilisateur est orienté vers son stock sauf quand une option significativement meilleure existe en magasin.

### 6.3 Composition multicouche (profil sportif / compétition)

Pour les profils multi-couches, le moteur exécute le scoring sur les deux pools (stock + marques favorites) puis compose et fusionne les combinaisons.

**Profil Sportif (2 couches) :**
```
Pour chaque pool (A et B) :
    slot_base = top 5 candidats avec role ∋ "base"
    slot_day  = top 5 candidats avec role ∋ "day_wax"
    combinaisons_pool = slot_base × slot_day
```

**Profil Compétition (3 couches) :**
```
Pour chaque pool (A et B) :
    slot_base     = top 5 candidats role ∋ "base"
    slot_day      = top 5 candidats role ∋ "day_wax"
    slot_topcoat  = top 5 candidats role ∋ "top_coat"
    combinaisons_pool = slot_base × slot_day × slot_topcoat
```

**Score combinaison :**
```
score_combo = Σ score_produit[i] × poids_couche[i]
            + bonus_disponibilite

Poids couches (sportif) : base = 0.35, day_wax = 0.65
Poids couches (compétition) : base = 0.25, day_wax = 0.45, top_coat = 0.30

bonus_disponibilite :
    100% en stock  → +10
    partiel        → +3
    rien en stock  → +0
```

**Fusion et classement :**

Les combinaisons des deux pools sont fusionnées et dédoublonnées. Le podium est ensuite composé selon la règle du slot garanti (voir §7.1) : si l'inventaire est non vide, la meilleure combo 100% en stock occupe toujours le premier slot, les slots suivants étant remplis par les meilleures combos tous pools confondus.

**Validation de cohérence :**
- Les plages de température des couches doivent se chevaucher d'au moins 3°C
- Alerte si base froide + top coat chaud (ou inversement)
- Alerte si même produit utilisé sur deux slots

### 6.4 Apple Intelligence — Scoring enrichi

Lorsque le framework Foundation Models est disponible (`SystemLanguageModel.default.isAvailable`), le moteur peut soumettre le contexte au LLM embarqué pour enrichir le scoring.

**Entrée du prompt :**
```
Conditions: temp_air=-8°C, humidity=45%, snow_type=[compact_glazed, artificial]
Top 5 candidates after algo scoring:
  1. Swix HS7 Violet (score: 87) — base+day_wax, -2/-8°C, humidity 25-70%
  2. Rex NF21 Blue (score: 84) — day_wax+base, -2/-8°C
  3. Toko WC HP Cold (score: 81) — day_wax, -10/-30°C, humidity 0-60%
  ...
Profile: sport (2 layers)
Inventory: [list of products in stock]
```

**Sortie attendue (JSON structuré) :**
```json
{
  "adjustments": [
    {"id": "swix-hs7-violet", "delta": +3, "reason": "Optimal pour neige artificielle compacte à cette humidité"},
    {"id": "toko-wc-hp-cold", "delta": -5, "reason": "Plage de température trop froide, risque de sous-performance"}
  ],
  "comment": "Conditions typiques de début de saison..."
}
```

Le delta Apple Intelligence est plafonné à ±10 points pour éviter que le LLM ne renverse complètement le scoring algorithmique. Le score final devient :

```
score_enrichi = score_algo + clamp(delta_AI, -10, +10)
```

**Fallback :** Si Apple Intelligence indisponible → scoring algorithmique seul. Aucune dégradation fonctionnelle.

---

## 7. Résultat et affichage

### 7.1 Écran podium

L'écran principal de résultat affiche un podium de 3 recommandations (ou 3 combinaisons multicouche), mêlant combos en stock et combos nécessitant un achat.

**Règle de composition du podium :**

Si l'utilisateur a un inventaire non vide, **le slot n°1 est toujours réservé à la meilleure combinaison 100% en stock**, quel que soit son score. Les slots 2 et 3 sont remplis par les meilleures combinaisons tous pools confondus (stock ou marques favorites), triées par score décroissant et dédoublonnées.

```
Si inventaire non vide :
    slot_1 = meilleure combo 100% en stock (score le plus élevé du Pool A)
    slot_2 = meilleure combo tous pools (hors doublon avec slot 1)
    slot_3 = 2e meilleure combo tous pools (hors doublons)

Si inventaire vide :
    slot_1, slot_2, slot_3 = top 3 du Pool B (marques favorites)
```

Cela garantit que l'utilisateur voit toujours ce qu'il peut faire immédiatement — même si le score est modeste — tout en découvrant de meilleures options à acheter dans les slots suivants. Si la meilleure combo en stock est aussi la meilleure tous pools confondus, elle occupe naturellement le slot 1 et les slots 2-3 montrent les alternatives.

**Affichage du slot 1 "stock" :** le label "Avec votre stock" (ou "From your stock" en anglais) est affiché au-dessus du slot 1 pour le distinguer clairement. Si le score est faible (< 50), un message contextuel prévient : *"Meilleure option disponible dans votre stock — les conditions actuelles ne sont pas idéales pour vos farts. Voici de meilleures options à acquérir."*

**Pour chaque recommandation :**
- Rang (1er, 2e, 3e) avec indicateur visuel
- Nom du/des produit(s) + marque
- Image produit (depuis `image_url`)
- Score de compatibilité (jauge circulaire 0–100)
- **Badge de disponibilité** :
  - 🟢 "Prêt" — tous les produits sont en stock
  - 🟡 "1 produit à acheter" — combo partiellement en stock, avec indication du produit manquant
  - 🔵 "À acheter" — aucun produit en stock
- Badge "IA" si le scoring a été enrichi par Apple Intelligence
- Indicateur éco si applicable

**En mode multicouche :** chaque recommandation est un groupe (ex. "Base: Swix HS7 + Glisse: Rex NF21") avec le score combiné. Chaque produit de la combo affiche son propre indicateur de stock.

### 7.2 Protocole détaillé (au tap)

Au tap sur une recommandation, l'écran de détail affiche le protocole complet de fartage :

**Section 1 — Produit(s)**
- Photo, nom complet, marque, gamme
- Lien vers la fiche fabricant (`product_url` → Safari)
- Plage de température, types de neige compatibles
- Indicateur de stock + statut

**Section 2 — Protocole d'application**

Pour chaque couche (du bas vers le haut) :

| Étape | Détail |
|---|---|
| Préparation | Brosser la semelle (brosse bronze/nylon selon état) |
| Application | Selon `format_type` : fer (`block_hot`, `powder_hot`) / liquide (`liquid`) / spray (`liquid_spray`) / rub-on (`block_rub`, `paste_rub`) |
| Température fer | `iron_temp_c`°C (si applicable) |
| Technique | Appliquer en couche fine, passes régulières |
| Refroidissement | ~15 min à température ambiante |
| Raclage | Racler excédent (racloir plexiglas) |
| Brossage | Brosse nylon (sens spatule → talon) |
| Finition | Polir au Fiberlene ou brosse douce |

Pour les liquides/sprays : appliquer, laisser sécher 2-5 min, brosser.

**Section 3 — Commentaire Apple Intelligence**

Si disponible, un paragraphe contextuel en langage naturel expliquant pourquoi cette recommandation est adaptée, les points d'attention et les alternatives. Affiché dans un encart distinct avec badge "IA".

Exemple : *"Le Swix HS7 est un excellent choix pour ces conditions : la neige artificielle compacte à -8°C avec 45% d'humidité est pile dans sa zone optimale. En deuxième couche, le Rex NF21 apportera de la vitesse supplémentaire. Attention, si l'humidité monte au-dessus de 60% dans l'après-midi, le HS10 Yellow serait un meilleur choix pour le top coat."*

### 7.3 Actions depuis le résultat

- **Ajouter au stock** : si le produit recommandé n'est pas en stock
- **Acheter** : lien vers `product_url` (site fabricant)
- **Partager** : export du protocole (texte formaté / image)
- **Historique** : sauvegarder la recommandation avec date, lieu et conditions (pour apprentissage futur)

---

## 8. Écrans de l'application

### 8.1 Navigation

```
TabBar
├── Recommandation (écran principal)
├── Mon Stock (inventaire)
└── Réglages
```

### 8.2 Écran Recommandation

**État initial (pas de conditions saisies) :**
- Carte WeatherKit avec conditions actuelles au lieu détecté
- Sélecteur de lieu (GPS actuel / recherche station / favoris)
- Champs température et humidité pré-remplis (WeatherKit), éditables
- Sélecteur type de neige (grille d'icônes)
- Bouton "Recommander"

**État résultat :**
- Podium 3 recommandations (mix stock + marques favorites)
- Filtre optionnel "Stock uniquement" pour ne voir que les combos 100% disponibles
- Résumé conditions en haut (température, humidité, neige — tap pour modifier)

### 8.3 Écran Mon Stock

- Liste des farts en stock, groupés par marque
- Indicateur visuel du statut (new / opened / almost empty)
- Recherche et filtres (marque, rôle, température)
- Bouton "+" pour ajouter (recherche dans le catalogue)
- Swipe pour supprimer
- Compteur total : "12 farts en stock"

### 8.4 Écran Réglages

- Profil (loisir / sportif / compétition)
- Marques autorisées (multi-sélection avec tout cocher/décocher)
- Préférence éco
- Conformité FIS
- Unités (°C / °F)
- Langue (FR / EN)
- À propos (version, crédits base de données, licences)

---

## 9. Stack technique

| Composant | Technologie |
|---|---|
| UI | SwiftUI |
| Persistance locale | SwiftData |
| Météo | WeatherKit |
| Géolocalisation | CoreLocation |
| LLM embarqué | Foundation Models (Apple Intelligence) |
| Base farts | JSON embarqué (Bundle) |
| Gestion projet | Tuist |
| Langue | Swift 6, concurrency stricte |
| Cible | iOS 26 minimum (Foundation Models) |
| Distribution | App Store |

### 9.1 Tuist — Gestion du projet Xcode

Le projet Xcode est généré et maintenu via **Tuist**. Aucun fichier `.xcodeproj` ou `.xcworkspace` n'est versionné dans Git — ils sont générés à la demande via `tuist generate`.

**Pourquoi Tuist :**
- Élimine les conflits de merge sur les fichiers `.pbxproj` (binaires, illisibles)
- Décrit le projet en Swift pur (`Project.swift`), versionnable et reviewable
- Accélère les builds via le cache de modules (`tuist cache`)
- Facilite l'ajout de cibles (tests, extensions, widgets futures) sans manipuler Xcode manuellement
- Intégration CI simplifiée : `tuist generate && xcodebuild`

**Structure Tuist prévue :**

```
Tuist/
  Config.swift              // Config globale (compatibilité, cloud…)
  Package.swift             // Dépendances SPM (si nécessaire)

Project.swift               // Déclaration du projet principal

wax.json/                   // Submodule Git (https://github.com/adhumi/wax.json)
  glide_wax.json            // Base de données (source of truth)
  glide_wax_schema.json     // Schéma de validation

Targets/
  GlideWax/
    Sources/                // Code principal de l'app
    Resources/              // Ressources propres à l'app (images, xcstrings…)
    Tests/                  // Tests unitaires
```

Le fichier `glide_wax.json` et son schéma ne sont **pas dupliqués** dans `Resources/`. Ils sont référencés directement depuis le submodule dans `Project.swift` via les `ResourceFileElements` :

```swift
// Dans Project.swift — ressources du target GlideWax
resources: [
    "Targets/GlideWax/Resources/**",
    "wax.json/glide_wax.json",
    "wax.json/glide_wax_schema.json"
]
```

Cela garantit que la base de données est toujours synchronisée avec le repo source (`git submodule update --remote` pour tirer la dernière version).

**Targets déclarés dans `Project.swift` :**

| Target | Type | Dépendances |
|---|---|---|
| `GlideWax` | `.app` | SwiftUI, SwiftData, WeatherKit, CoreLocation, FoundationModels |
| `GlideWaxTests` | `.unitTests` | `GlideWax` |
| `GlideWaxUITests` | `.uiTests` | `GlideWax` |

Le target principal déclare `CFBundleDisplayName = "Glide Wax"` dans son `infoPlist` pour que le nom affiché sur l'écran d'accueil et l'App Store soit "Glide Wax" (avec espace).

**Validation JSON en phase Build :**

Un script de build Tuist exécute la validation du JSON contre le schéma à chaque build (fail-fast si le catalogue est corrompu) :

```swift
// Dans Project.swift — script de validation
.pre(
    script: """
    python3 -m jsonschema \
        --instance "${SRCROOT}/wax.json/glide_wax.json" \
        "${SRCROOT}/wax.json/glide_wax_schema.json"
    """,
    name: "Validate Wax Database",
    basedOnDependencyAnalysis: false
)
```

**Workflow développeur :**

```bash
# Première installation
curl -Ls https://install.tuist.io | bash

# Cloner avec le submodule
git clone --recursive <repo-url>
# ou après un clone classique :
git submodule update --init

# Générer le projet Xcode
tuist generate

# Ouvrir dans Xcode (généré à la volée)
open GlideWax.xcworkspace

# Mettre à jour la base de données (nouvelle version du JSON)
git submodule update --remote wax.json
```

Le fichier `.gitignore` exclut `*.xcodeproj`, `*.xcworkspace` et `Derived/`. Le dossier `wax.json/` n'est pas dans `.gitignore` — il est géré par `.gitmodules`. Seuls les fichiers Tuist (`Project.swift`, `Config.swift`) et les sources sont versionnés.

### 9.2 Offline-first

L'app fonctionne intégralement hors connexion :
- Base de données JSON embarquée
- Inventaire en SwiftData local
- Scoring algorithmique sans réseau
- Seuls WeatherKit et Apple Intelligence nécessitent une connexion (graceful fallback)

---

## 10. Modèle de données Swift

### 10.1 Types alignés sur le JSON Schema

```swift
// MARK: - Localization

/// Matches the JSON Schema's LocalizedString: a dictionary keyed by locale
/// (pattern: xx_XX), with fr_FR guaranteed present. Values may be null
/// (translation pending).
struct LocalizedString: Codable, Equatable {
    let values: [String: String?]

    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        values = try container.decode([String: String?].self)
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        try container.encode(values)
    }

    /// Returns the best available translation for the current locale.
    /// Fallback chain: exact match → language match → fr_FR (always present).
    func localized(for locale: Locale = .current) -> String {
        let langCode = locale.language.languageCode?.identifier ?? "fr"

        // 1. Exact locale match (e.g. "en_US")
        let exactKey = "\(langCode)_\(locale.region?.identifier ?? "")"
        if let val = values[exactKey], let str = val { return str }

        // 2. Language-level match (first key starting with "en_")
        if let match = values.first(where: { $0.key.hasPrefix("\(langCode)_") }),
           let str = match.value { return str }

        // 3. Guaranteed fallback (fr_FR is required by schema)
        return values["fr_FR"].flatMap { $0 } ?? ""
    }
}

// MARK: - Catalogue

struct WaxProduct: Codable, Identifiable {
    let id: String
    let name: String
    let brand: String
    let productLine: String
    let formatType: FormatType
    let tempMinC: Int?
    let tempMaxC: Int?
    let ironTempC: Int?
    let snowType: [SnowType]
    let level: Level
    let fluorinated: Bool
    let fisCompliant: Bool
    let comment: LocalizedString
    let imageUrl: String
    let role: [WaxRole]
    let humidityMin: Int?
    let humidityMax: Int?
    let eco: Bool
    let durabilityKm: Int?
    let productUrl: String
    let dateAdded: String
    let dateUpdated: String
    let active: Bool
    let humiditySource: HumiditySource?

    enum CodingKeys: String, CodingKey {
        case id, name, brand, eco, role, active, level, fluorinated, comment
        case productLine = "product_line"
        case formatType = "format_type"
        case tempMinC = "temp_min_c"
        case tempMaxC = "temp_max_c"
        case ironTempC = "iron_temp_c"
        case snowType = "snow_type"
        case fisCompliant = "fis_compliant"
        case imageUrl = "image_url"
        case humidityMin = "humidity_min"
        case humidityMax = "humidity_max"
        case durabilityKm = "durability_km"
        case productUrl = "product_url"
        case dateAdded = "date_added"
        case dateUpdated = "date_updated"
        case humiditySource = "humidity_source"
    }
}

// MARK: - Enums (alignées sur le JSON Schema)

enum SnowType: String, Codable, CaseIterable {
    case heavyNew = "heavy_new"
    case artificial
    case freshFalling = "fresh_falling"
    case fineFresh = "fine_fresh"
    case mixedNewDirtyBase = "mixed_new_dirty_base"
    case compact
    case compactGlazed = "compact_glazed"
    case compactDirty = "compact_dirty"
    case transformed
    case wet
    case dryGrain = "dry_grain"
    case wetGrain = "wet_grain"
}

enum FormatType: String, Codable, CaseIterable {
    case blockHot = "block_hot"
    case blockRubRoto = "block_rub_roto"
    case blockRub = "block_rub"
    case liquid
    case liquidSpray = "liquid_spray"
    case powderHot = "powder_hot"
    case powder
    case pasteRub = "paste_rub"

    /// Whether this format requires a waxing iron
    var requiresIron: Bool {
        switch self {
        case .blockHot, .powderHot: return true
        default: return false
        }
    }
}

enum Level: String, Codable, CaseIterable {
    case beginner, sport, expert
}

enum WaxRole: String, Codable, CaseIterable {
    case basePrep = "base_prep"
    case base
    case dayWax = "day_wax"
    case topCoat = "top_coat"
    case universal
    case cleaner
    case additive
}

enum HumiditySource: String, Codable {
    case manufacturer
    case colorInference = "color_inference"
    case community
}

// MARK: - Inventaire

@Model
class WaxInventoryItem {
    var waxId: String           // Référence vers product.id
    var dateAdded: Date
    var status: StockStatus
    var notes: String?

    init(waxId: String, status: StockStatus = .new) { ... }
}

enum StockStatus: String, Codable {
    case new = "new"
    case opened
    case almostEmpty = "almost_empty"
}

// MARK: - Conditions

struct WaxingConditions {
    var temperature: Double        // °C
    var humidity: Double           // % (0-100)
    var snowTypes: [SnowType]
    var location: String?
    var weatherSource: WeatherSource
    var date: Date
}

enum WeatherSource {
    case weatherKit
    case manual
    case mixed   // WeatherKit + override partiel
}

// MARK: - Profil

enum UserProfile: String, Codable {
    case leisure       // 1 couche
    case sport         // 2 couches
    case competition   // 3 couches
}

// MARK: - Résultat

struct WaxRecommendation: Identifiable {
    let id = UUID()
    let layers: [RecommendedLayer]
    let scoreTotal: Double           // 0-100 (incluant bonus disponibilité)
    let scoreTechnique: Double       // 0-100 (avant bonus disponibilité)
    let availability: Availability
    let aiEnhanced: Bool
    let aiComment: LocalizedString?
}

enum Availability {
    case ready              // 100% en stock → bonus +10
    case partial(missing: [WaxProduct])  // partiel → bonus +3
    case toShop             // rien en stock → bonus +0
}

struct RecommendedLayer {
    let role: WaxRole
    let product: WaxProduct
    let score: Double
    let inStock: Bool
    let stockStatus: StockStatus?
}
```

### 10.2 Tables de traduction des enums

Les enums sont stockées en anglais dans le JSON. L'app les traduit pour l'affichage via des extensions localisées utilisant le système `String(localized:)` de Foundation :

```swift
extension SnowType {
    var localizedName: String {
        switch self {
        case .heavyNew: String(localized: "snow.heavy_new", defaultValue: "Heavy new")
        case .artificial: String(localized: "snow.artificial", defaultValue: "Artificial")
        case .freshFalling: String(localized: "snow.fresh_falling", defaultValue: "Fresh falling")
        case .compact: String(localized: "snow.compact", defaultValue: "Compact")
        // ... etc.
        }
    }
}

extension FormatType {
    var localizedName: String {
        switch self {
        case .blockHot: String(localized: "format.block_hot", defaultValue: "Hot wax block")
        case .liquid: String(localized: "format.liquid", defaultValue: "Liquid")
        case .liquidSpray: String(localized: "format.liquid_spray", defaultValue: "Liquid spray")
        case .pasteRub: String(localized: "format.paste_rub", defaultValue: "Paste (rub-on)")
        // ... etc.
        }
    }
}
```

Les traductions françaises sont fournies dans `Localizable.xcstrings` (format Xcode 15+). Ce mécanisme permet d'ajouter de nouvelles langues (DE, NO, FI…) sans modifier le JSON ni le code — uniquement en ajoutant des fichiers de traduction.

---

## 11. Apple Intelligence — Intégration détaillée

### 11.1 Disponibilité

```swift
import FoundationModels

var aiAvailable: Bool {
    SystemLanguageModel.default.isAvailable
}
```

Si `false` → fallback algorithmique pur. Aucun message d'erreur, l'app fonctionne normalement sans badge "IA".

### 11.2 Prompt scoring enrichi

Utilisé après le scoring algorithmique pour ajuster les scores du top 5 :

```swift
func enrichScoring(candidates: [ScoredCandidate], conditions: WaxingConditions) async -> [ScoreAdjustment]? {
    guard aiAvailable else { return nil }

    let session = SystemLanguageModel.default.session(instructions: """
        Tu es un expert en fartage de ski de fond.
        Analyse les conditions et les candidats. Pour chaque candidat,
        propose un ajustement de score (delta entre -10 et +10)
        avec une justification courte.
        Réponds uniquement en JSON.
        Langue de réponse : \(Locale.current.language.languageCode == "en" ? "English" : "Français").
        """)

    let prompt = buildScoringPrompt(candidates: candidates, conditions: conditions)
    let response = try? await session.respond(to: prompt)
    return parseAdjustments(response)
}
```

### 11.3 Prompt commentaire

Utilisé pour générer le texte contextuel affiché dans le protocole détaillé :

```swift
func generateComment(recommendation: WaxRecommendation, conditions: WaxingConditions) async -> String? {
    guard aiAvailable else { return nil }

    let lang = Locale.current.language.languageCode == "en" ? "English" : "Français"
    let session = SystemLanguageModel.default.session(instructions: """
        Tu es un technicien de fartage expérimenté. Commente cette
        recommandation en 2-3 phrases : pourquoi c'est adapté,
        points d'attention, et alternative si les conditions changent.
        Ton naturel et pratique, pas de jargon inutile.
        Réponds en \(lang).
        """)

    let prompt = buildCommentPrompt(recommendation: recommendation, conditions: conditions)
    let response = try? await session.respond(to: prompt)
    return response?.content
}
```

### 11.4 Gestion d'erreurs

- Timeout : 5 secondes max → fallback algo
- Réponse non parsable : ignorer, afficher résultat algo
- Modèle non chargé : afficher résultat algo sans délai
- Jamais de blocage de l'UI en attente du LLM

---

## 12. Hors scope V1

| Fonctionnalité | Raison | Cible |
|---|---|---|
| Synchronisation iCloud du stock | Complexité backend | V2 |
| Scan visuel produit (caméra) | Nécessite modèle ML dédié | V2 |
| Historique avec feedback ("ça a bien marché") | Boucle d'apprentissage | V2 |
| Fart de retenue (grip) | Base de données à construire | V2 |
| watchOS / macOS | Prioriser l'expérience iPhone | V2 |
| Intégration Arnuva | Standalone d'abord | V3 |
| Recommandation par météo prévisionnelle (J+1, J+2) | Complexité UX | V2 |
| Achat in-app / liens affiliés | Modèle économique à définir | V2 |
| Contributions communautaires (ajout produits) | Modération nécessaire | V3 |

---

## 13. Métriques de succès V1

| Métrique | Objectif |
|---|---|
| Temps moyen jusqu'à recommandation | < 15 secondes (depuis ouverture) |
| Couverture scoring température | ≥ 95% des candidats scorés (non null) |
| Précision perçue | ≥ 4/5 étoiles feedback utilisateur |
| Crash rate | < 0.1% sessions |
| Fonctionnement offline | 100% fonctionnel (hors WeatherKit/AI) |
