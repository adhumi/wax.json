# Contribuer a wax.json

Merci de votre interet pour ce projet ! Voici comment contribuer au catalogue de farts de glisse.

## Ajouter ou modifier un fart

1. **Forkez** le depot et creez une branche depuis `main`.
2. Editez le fichier `glide_wax.json` en respectant le schema `glide_wax_schema.json`.
3. Validez vos modifications localement :
   ```bash
   pip install check-jsonschema
   check-jsonschema --schemafile glide_wax_schema.json glide_wax.json
   ```
4. Ouvrez une **pull request** vers `main`.

## Structure d'un produit

Chaque entree dans le tableau `products` doit contenir les champs obligatoires suivants :

| Champ | Type | Description |
|---|---|---|
| `id` | string | Identifiant unique (slug en minuscules, tirets) |
| `name` | string | Nom commercial du produit |
| `brand` | string | Marque |
| `product_line` | string | Gamme ou ligne de produit |
| `format_type` | enum | `block_hot`, `block_rub_roto`, `block_rub`, `liquid`, `liquid_spray`, `powder_hot`, `powder`, `paste_rub` |
| `temp_min_c` | int ou null | Temperature minimale en °C |
| `temp_max_c` | int ou null | Temperature maximale en °C |
| `iron_temp_c` | int ou null | Temperature du fer en °C (null si sans fer) |
| `snow_type` | array | Types de neige (voir le schema pour les valeurs possibles) |
| `level` | enum | `beginner`, `sport`, `expert` |
| `role` | array | `base_prep`, `base`, `day_wax`, `top_coat`, `universal`, `cleaner`, `additive` |
| `fluorinated` | boolean | Toujours `false` (catalogue sans fluor uniquement) |
| `fis_compliant` | boolean | Conforme a la reglementation FIS |
| `humidity_min` | int ou null | Humidite relative minimale (%) |
| `humidity_max` | int ou null | Humidite relative maximale (%) |
| `humidity_source` | enum ou null | `manufacturer`, `color_inference`, `community` |
| `eco` | boolean | Produit eco-responsable / biodegradable |
| `durability_km` | int ou null | Durabilite estimee en km |
| `comment` | object | Commentaire localise (`{"fr_FR": "..."}` minimum) |
| `image_url` | string (URI) | URL de l'image du produit |
| `product_url` | string (URI) | URL de la fiche produit |
| `date_added` | date | Date d'ajout (format YYYY-MM-DD) |
| `date_updated` | date | Date de derniere mise a jour |
| `active` | boolean | Produit toujours commercialise |

## Regles

- **Pas de fluor** : seuls les farts sans fluor sont acceptes.
- **Sources verifiables** : les donnees doivent provenir de sources publiques (sites fabricants, fiches techniques).
- **Un produit = un `id` unique** : utilisez le format `marque-nom-en-minuscules` avec des tirets.
- **Commentaire en francais obligatoire** : le champ `comment` doit contenir au minimum une cle `fr_FR`.

## Signaler une erreur

Si vous constatez une erreur dans les donnees (temperature, format, etc.), ouvrez une **issue** en precisant :
- Le nom et la marque du produit concerne
- Le champ incorrect et la valeur attendue
- Une source pour verifier la correction

## Generation de la page HTML

La page `index.html` est generee automatiquement par la CI. Vous n'avez pas besoin de la modifier. Si vous souhaitez tester localement :

```bash
python generate_index.py
```

Cela regenerera `index.html` a partir de `glide_wax.json`.
