# wax.json

Catalogue open-source de farts de glisse sans fluor pour le ski de fond, au format JSON.

Le fichier `glide_wax.json` recense **191 produits** de **22 marques** avec leurs plages de température, types de neige, formats, niveaux et plus encore. Un schéma JSON (`glide_wax_schema.json`) garantit la cohérence des données et une CI GitHub Actions valide chaque modification.

## Fichiers du projet

| Fichier | Description |
|---|---|
| `glide_wax.json` | Catalogue complet des farts (source de vérité) |
| `glide_wax_schema.json` | Schéma JSON (draft 2020-12) pour la validation |
| `generate_index.py` | Script Python pour générer `index.html` à partir du JSON |
| `index.html` | Page HTML consultable (générée automatiquement par la CI) |

## Catalogue des farts

| Marque | Nom | Gamme | Format | Température | Niveau | Eco |
|---|---|---|---|---|---|---|
| Swix | PS Polar | Performance Speed (PS) | Bloc (fer) | -32 / -14 °C | Sport | |
| Swix | PS5 Turquoise | Performance Speed (PS) | Bloc (fer) | -18 / -10 °C | Sport | |
| Swix | PS6 Blue | Performance Speed (PS) | Bloc (fer) | -12 / -6 °C | Sport | |
| Swix | PS7 Violet | Performance Speed (PS) | Bloc (fer) | -8 / -2 °C | Sport | |
| Swix | PS8 Red | Performance Speed (PS) | Bloc (fer) | -4 / 4 °C | Sport | |
| Swix | PS10 Yellow | Performance Speed (PS) | Bloc (fer) | 0 / 10 °C | Sport | |
| Swix | HS5 Turquoise | High Speed (HS) | Bloc (fer) | -18 / -10 °C | Expert | |
| Swix | HS6 Blue | High Speed (HS) | Bloc (fer) | -12 / -6 °C | Expert | |
| Swix | HS7 Violet | High Speed (HS) | Bloc (fer) | -8 / -2 °C | Expert | |
| Swix | HS8 Red | High Speed (HS) | Bloc (fer) | -4 / 4 °C | Expert | |
| Swix | HS10 Yellow | High Speed (HS) | Bloc (fer) | 0 / 10 °C | Expert | |
| Swix | F4 Glidewax (bloc) | Universal | Bloc (fer) | — | Debutant | Oui |
| Swix | F4 Glidewax Rub-on | Universal | Pate | — | Debutant | Oui |
| Swix | F4 Glidewax Paste | Universal | Pate | — | Debutant | Oui |
| Swix | U60 / U180 Universal Wax | Universal | Bloc (fer) | — | Debutant | |
| Swix | BP77 Base Prep Hard | Base Prep | Bloc (fer) | -32 / -10 °C | Expert | |
| Swix | BP88 Base Prep Medium | Base Prep | Bloc (fer) | -10 / 0 °C | Expert | |
| Swix | BP99 Base Prep Soft | Base Prep | Bloc (fer) | 0 / 1 °C | Expert | |
| Toko | Base Performance Yellow | Base Performance | Bloc (fer) | -6 / 0 °C | Debutant | Oui |
| Toko | Base Performance Red | Base Performance | Bloc (fer) | -12 / -4 °C | Debutant | Oui |
| Toko | Base Performance Blue | Base Performance | Bloc (fer) | -30 / -10 °C | Debutant | Oui |
| Toko | Base Performance Cleaning | Base Performance | Bloc (fer) | — | Debutant | Oui |
| Toko | Performance Yellow | Performance | Bloc (fer) | -6 / 0 °C | Sport | |
| Toko | Performance Red | Performance | Bloc (fer) | -12 / -4 °C | Sport | |
| Toko | Performance Blue | Performance | Bloc (fer) | -30 / -10 °C | Sport | |
| Toko | WC High Performance Warm (Yellow) | WC High Performance | Bloc (fer) | -3 / 0 °C | Expert | |
| Toko | WC High Performance Universal (Red) | WC High Performance | Bloc (fer) | -12 / -4 °C | Expert | |
| Toko | WC High Performance Cold (Blue) | WC High Performance | Bloc (fer) | -30 / -10 °C | Expert | |
| Toko | Jet Liquid Yellow | Jet Liquid (top finish) | Spray | -4 / 0 °C | Expert | |
| Toko | Jet Liquid Red | Jet Liquid (top finish) | Spray | -12 / -2 °C | Expert | |
| Toko | Jet Liquid Blue | Jet Liquid (top finish) | Spray | -20 / -10 °C | Expert | |
| Toko | Jet Bloc Top Finish Warm | Jet Bloc (top finish) | Bloc (frottement/roto) | -2 / 0 °C | Expert | |
| Toko | Jet Bloc Top Finish Mid | Jet Bloc (top finish) | Bloc (frottement/roto) | -12 / -2 °C | Expert | |
| Toko | Jet Bloc Top Finish Cold | Jet Bloc (top finish) | Bloc (frottement/roto) | -30 / -10 °C | Expert | |
| Holmenkol | Syntec FF Bar Green | Syntec FF | Bloc (fer) | -30 / -15 °C | Expert | |
| Holmenkol | Syntec FF Bar Blue | Syntec FF | Bloc (fer) | -15 / -8 °C | Expert | |
| Holmenkol | Syntec FF Bar Red | Syntec FF | Bloc (fer) | -10 / -4 °C | Expert | |
| Holmenkol | Syntec FF Bar Yellow | Syntec FF | Bloc (fer) | -4 / 0 °C | Expert | |
| Holmenkol | Syntec FF 21 (Base Wax) | Syntec FF | Bloc (fer) | -20 / 0 °C | Expert | |
| Holmenkol | UltraMix Blue (Liquid) | Liquid Wax | Liquide | -20 / -8 °C | Sport | |
| Holmenkol | BetaMix Red (Liquid) | Liquid Wax | Liquide | -14 / -4 °C | Sport | |
| Holmenkol | AlphaMix Yellow (Liquid) | Liquid Wax | Liquide | -4 / 0 °C | Sport | |
| Holmenkol | BetaMix Red (Bloc) | BetaMix | Bloc (fer) | -14 / -4 °C | Sport | |
| Holmenkol | Natural Skiwax | Natural | Bloc (fer) | — | Debutant | Oui |
| Rex | NF11 Yellow | NF (N-Kinetic Fluor-Free) | Poudre (fer) | -2 / 10 °C | Expert | |
| Rex | NF21 Blue | NF (N-Kinetic Fluor-Free) | Poudre (fer) | -12 / -2 °C | Expert | |
| Rex | NF21G Black (New Snow) | NF (N-Kinetic Fluor-Free) | Poudre (fer) | -12 / 2 °C | Expert | |
| Rex | NF31 Green | NF (N-Kinetic Fluor-Free) | Poudre (fer) | -20 / -8 °C | Expert | |
| Rex | NF41 Pink/Green | NF (N-Kinetic Fluor-Free) | Poudre (fer) | -20 / 5 °C | Expert | |
| Rex | G11 Yellow Spray | G-Series Spray | Spray | -2 / 10 °C | Expert | |
| Rex | G21 Blue Spray | G-Series Spray | Spray | -12 / -2 °C | Expert | |
| Rex | G41 UHW Pink/Green Spray | G-Series Spray | Spray | -20 / 5 °C | Expert | |
| Rex | Gold Liquid | Gold | Spray | — | Expert | |
| Rex | Original Blue (Liquid) | Original Liquid Glider | Liquide | -15 / -2 °C | Sport | |
| Rex | Original Purple (Liquid) | Original Liquid Glider | Liquide | -2 / 5 °C | Sport | |
| Rex | Blue (Bloc) | Original Glide Wax | Bloc (fer) | -10 / -1 °C | Sport | |
| Vauhti | Pure Pro Warm (Liquid) | Pure Pro | Liquide | -3 / 7 °C | Sport | |
| Vauhti | Pure Pro Cold (Liquid) | Pure Pro | Liquide | -20 / -2 °C | Sport | |
| Vauhti | Pure Pro LDR (Liquid) | Pure Pro | Liquide | -10 / 5 °C | Sport | |
| Vauhti | Pure Pro Mid (Liquid) | Pure Pro | Liquide | -4 / 2 °C | Sport | |
| Vauhti | Pure Pro Wet (Liquid) | Pure Pro | Liquide | -1 / 10 °C | Sport | |
| Vauhti | Race Violet Liquid Glide | Race Liquid Glide | Liquide | -7 / -1 °C | Expert | |
| Vauhti | Race Red Liquid Glide | Race Liquid Glide | Liquide | -3 / 7 °C | Expert | |
| Vauhti | Race Pink Liquid Glide | Race Liquid Glide | Liquide | -4 / 3 °C | Expert | |
| Vauhti | Race Green Liquid Glide | Race Liquid Glide | Liquide | -20 / -10 °C | Expert | |
| Vauhti | Race Blue Liquid Glide | Race Liquid Glide | Liquide | -15 / -5 °C | Expert | |
| Vauhti | ONE Warm | ONE | Bloc (fer) | -3 / 7 °C | Debutant | |
| Vauhti | ONE Cold | ONE | Bloc (fer) | -20 / -2 °C | Debutant | |
| Vauhti | ONE LDR | ONE | Bloc (fer) | -10 / 5 °C | Debutant | |
| Start | SG6 Red | SG (Start Glider) | Bloc (fer) | -7 / 0 °C | Sport | |
| Start | SG8 Purple | SG (Start Glider) | Bloc (fer) | -7 / -2 °C | Sport | |
| Start | SG9 Blue | SG (Start Glider) | Bloc (fer) | -12 / -7 °C | Sport | |
| Start | SG10 Green | SG (Start Glider) | Bloc (fer) | -30 / -10 °C | Sport | |
| Start | RG Red | RG Racing Glider | Liquide | -2 / 10 °C | Expert | |
| Start | RG Purple | RG Racing Glider | Liquide | -5 / 5 °C | Expert | |
| Start | RG Blue | RG Racing Glider | Liquide | -12 / -3 °C | Expert | |
| Star | NEXT Warm | NEXT | Bloc (fer) | -5 / 0 °C | Sport | Oui |
| Star | NEXT Medium | NEXT | Bloc (frottement/roto) | -8 / -3 °C | Sport | Oui |
| Star | NEXT Cold | NEXT | Bloc (fer) | -20 / -8 °C | Sport | Oui |
| Star | NF Warm (Liquid) | NF | Liquide | -5 / 0 °C | Sport | |
| Star | NF Medium (Liquid) | NF | Liquide | -8 / -3 °C | Sport | |
| Star | NF Cold (Liquid) | NF | Liquide | -20 / -5 °C | Sport | |
| Star | NF Polar (Bloc) | NF | Bloc (fer) | -30 / -10 °C | Sport | |
| mountainFLOW | Hot Wax All-Temp | Hot Wax | Bloc (fer) | -13 / -1 °C | Debutant | Oui |
| mountainFLOW | Hot Wax Warm | Hot Wax | Bloc (fer) | -1 / 5 °C | Debutant | Oui |
| mountainFLOW | Hot Wax Cool | Hot Wax | Bloc (fer) | -12 / -4 °C | Debutant | Oui |
| mountainFLOW | Hot Wax Cold | Hot Wax | Bloc (fer) | -21 / -9 °C | Debutant | Oui |
| mountainFLOW | Quick Wax Warm | Quick Wax | Pate | -1 / 5 °C | Debutant | Oui |
| mountainFLOW | Quick Wax Cool | Quick Wax | Pate | -10 / -1 °C | Debutant | Oui |
| Rode | R50 Yellow | R-Line Fluor Free | Bloc (fer) | -1 / 5 °C | Sport | |
| Rode | R52 Red | R-Line Fluor Free | Bloc (fer) | -4 / 0 °C | Sport | |
| Rode | R54 Blue | R-Line Fluor Free | Bloc (fer) | -12 / -3 °C | Sport | |
| Rode | R56 Green | R-Line Fluor Free | Bloc (fer) | -20 / -8 °C | Sport | |
| Rode | R100G Graphite | R-Line Fluor Free | Bloc (fer) | -30 / -5 °C | Sport | |
| Rode | RX22 World Cup | RX World Cup | Bloc (fer) | -20 / -8 °C | Expert | |
| Rode | RX32 World Cup | RX World Cup | Bloc (fer) | -10 / -4 °C | Expert | |
| Rode | RX42 World Cup | RX World Cup | Bloc (fer) | -5 / 0 °C | Expert | |
| Rode | RL Warm (Racing Liquid) | RL Racing Liquid | Liquide | -3 / 0 °C | Expert | Oui |
| Rode | RL Med (Racing Liquid) | RL Racing Liquid | Liquide | -7 / -2 °C | Expert | Oui |
| Rode | RL Cold (Racing Liquid) | RL Racing Liquid | Liquide | -15 / -5 °C | Expert | Oui |
| Gallium | Extra Base Violet | Extra Base | Bloc (fer) | -4 / 3 °C | Sport | |
| Gallium | Extra Base Blue | Extra Base | Bloc (fer) | -12 / -3 °C | Sport | |
| Gallium | Extra Base Green | Extra Base | Bloc (fer) | -20 / -10 °C | Sport | |
| Gallium | Metallic Ion Block | Metallic Ion NF | Bloc (fer) | -10 / 3 °C | Expert | |
| Gallium | Giga Speed BN Block NF | Giga Speed NF | Bloc (fer) | -12 / -2 °C | Expert | |
| Gallium | D-Control Anti Dirt | D-Control NF | Bloc (fer) | -5 / 5 °C | Expert | |
| Gallium | NF Liquid | NF Liquid | Liquide | -5 / 3 °C | Sport | |
| Briko-Maplus | BP1 Yellow | BP1 Base Paraffin | Bloc (fer) | -3 / 0 °C | Sport | |
| Briko-Maplus | BP1 Red | BP1 Base Paraffin | Bloc (fer) | -7 / -3 °C | Sport | |
| Briko-Maplus | BP1 Violet | BP1 Base Paraffin | Bloc (fer) | -12 / -5 °C | Sport | |
| Briko-Maplus | BP1 Blue | BP1 Base Paraffin | Bloc (fer) | -20 / -10 °C | Sport | |
| Briko-Maplus | Race Base Medium | Race Base | Bloc (fer) | -15 / 0 °C | Sport | |
| Optiwax | HydrOX Race Glider Warm | HydrOX Race | Bloc (fer) | -2 / 5 °C | Expert | |
| Optiwax | HydrOX Race Glider Mid | HydrOX Race | Bloc (fer) | -10 / 0 °C | Expert | |
| Optiwax | HydrOX Race Glider Cold | HydrOX Race | Bloc (fer) | -20 / -8 °C | Expert | |
| Optiwax | Glide Tape Eco | Glide Tape | Pate | -20 / 5 °C | Debutant | Oui |
| Purl | Purple All-Temp | Original | Bloc (fer) | -12 / 0 °C | Debutant | Oui |
| Purl | Blue Cold | Original | Bloc (fer) | -21 / -7 °C | Debutant | Oui |
| Purl | Yellow Warm | Original | Bloc (fer) | -2 / 5 °C | Debutant | Oui |
| Purl | Green Sub-Zero | Original | Bloc (fer) | -30 / -15 °C | Debutant | Oui |
| Purl | Black Graphite | Original | Bloc (frottement/roto) | -30 / -10 °C | Debutant | Oui |
| Purl | PRO Race Bar | PRO | Bloc (fer) | -12 / 0 °C | Expert | Oui |
| Hertel | Super HotSauce | Super HotSauce | Bloc (fer) | -14 / 11 °C | Debutant | Oui |
| Hertel | Racing 739 | Racing | Bloc (fer) | -14 / 11 °C | Expert | |
| Hertel | SpringSolution | SpringSolution | Bloc (fer) | -7 / 20 °C | Sport | |
| Hertel | Rub-N-Go | Super HotSauce | Pate | -14 / 11 °C | Debutant | Oui |
| Dominator | Zoom | Zoom | Bloc (fer) | -20 / 5 °C | Debutant | |
| Dominator | Graphite Zoom | Zoom | Bloc (fer) | -25 / 2 °C | Debutant | |
| Dominator | FFC 2 (Fluor Free Competition) | FFC | Bloc (fer) | -7 / 2 °C | Sport | Oui |
| Dominator | FFC 2C Cold | FFC | Bloc (fer) | -20 / -7 °C | Sport | Oui |
| Dominator | FFC P2 Paste | FFC | Pate | -7 / 2 °C | Sport | Oui |
| Fast Wax | HS 0 White (Extreme Cold) | High Speed | Bloc (fer) | -34 / -13 °C | Sport | |
| Fast Wax | HS 10 Teal (Cold) | High Speed | Bloc (fer) | -23 / -9 °C | Sport | |
| Fast Wax | HS 20 Blue (Mid) | High Speed | Bloc (fer) | -11 / -2 °C | Sport | |
| Fast Wax | HS 30 Red (Warm) | High Speed | Bloc (fer) | -5 / 3 °C | Sport | |
| Fast Wax | HS 40 Yellow (Spring) | High Speed | Bloc (fer) | -1 / 8 °C | Sport | |
| Fast Wax | HSX 20 Blue Paste | HSX Paste | Pate | -11 / -2 °C | Debutant | Oui |
| Fast Wax | Thunderbolt 10 | Thunderbolt | Bloc (fer) | -15 / -3 °C | Expert | Oui |
| DataWax | Universal All Mountain | All Mountain | Bloc (fer) | -20 / 5 °C | Debutant | |
| DataWax | Magma All Mountain (Fresh Snow) | All Mountain | Bloc (fer) | -10 / 3 °C | Debutant | |
| DataWax | Butane All Mountain (Cold Snow) | All Mountain | Bloc (fer) | -20 / -5 °C | Debutant | |
| DataWax | Cobalt All Mountain (Very Cold) | All Mountain | Bloc (fer) | -25 / -12 °C | Sport | |
| DataWax | Sunfire Race | Race | Bloc (fer) | -5 / 3 °C | Expert | |
| DataWax | Magma Race | Race | Bloc (fer) | -15 / -3 °C | Expert | |
| DataWax | Arctic Indoor Race Graphite | Arctic Indoor | Bloc (fer) | -5 / 0 °C | Expert | |
| ZUMWax | Universal All Temps | Iron-On | Bloc (fer) | -30 / 0 °C | Debutant | |
| ZUMWax | Warm Temps | Iron-On | Bloc (fer) | -6 / 0 °C | Debutant | |
| ZUMWax | Chill Temps | Iron-On | Bloc (fer) | -15 / -5 °C | Debutant | |
| ZUMWax | Cold Temps | Iron-On | Bloc (fer) | -30 / -10 °C | Debutant | |
| ZUMWax | Rub-On Universal | Rub-On | Pate | -30 / 0 °C | Debutant | |
| ZUMWax | Endurance Marathon | Endurance | Bloc (fer) | -20 / 0 °C | Sport | |
| Solda | HC1 Orange | HC1 Hydrocarbon | Bloc (fer) | -7 / 2 °C | Debutant | |
| Solda | HC1 Violet | HC1 Hydrocarbon | Bloc (fer) | -14 / -4 °C | Debutant | |
| Solda | HC1 Green | HC1 Hydrocarbon | Bloc (fer) | -24 / -7 °C | Debutant | |
| Solda | HC28 Carbon | HC28 | Bloc (fer) | -20 / 0 °C | Sport | |
| Solda | Superglide Yellow | Superglide New Era | Bloc (fer) | -4 / 5 °C | Expert | |
| Solda | Superglide Red | Superglide New Era | Bloc (fer) | -13 / 0 °C | Expert | |
| Solda | Superglide Green | Superglide New Era | Bloc (fer) | -24 / -13 °C | Expert | |
| Solda | Superspeed Paste | Superglide New Era | Pate | -10 / 5 °C | Sport | |
| Solda | HL4 Powder Mid | HL Powder | Poudre | -10 / 0 °C | Expert | |
| HWK | Racing Wax (Fluor Free) | Racing | Bloc (fer) | -10 / 10 °C | Expert | |
| HWK | Eco Allround Skiwax | ECO Line | Bloc (fer) | -10 / 10 °C | Debutant | Oui |
| HWK | Eco Liquo Skiwax | ECO Line | Liquide | -10 / 10 °C | Debutant | Oui |
| HWK | HX Racewax Newsnow Cold | HX High X | Bloc (fer) | -20 / -8 °C | Expert | |
| HWK | HX Racewax Newsnow Warm | HX High X | Bloc (fer) | -5 / 5 °C | Expert | |
| HWK | HX Racewax Oldsnow Cold | HX High X | Bloc (fer) | -20 / -8 °C | Expert | |
| HWK | HX Racewax Oldsnow Warm | HX High X | Bloc (fer) | -5 / 5 °C | Expert | |
| HWK | UHX Liquo Spray Warm | UHX Ultra High X | Liquide | -4 / 10 °C | Expert | |
| HWK | UHX Liquo Spray Cold | UHX Ultra High X | Liquide | -25 / -8 °C | Expert | |
| HWK | Speed Milk | Speed Milk | Liquide | -15 / 10 °C | Sport | |
| SkiGo | FFC Yellow (Fluor Free Competition) | FFC Competition | Bloc (fer) | -1 / 20 °C | Expert | |
| SkiGo | FFC Orange | FFC Competition | Bloc (fer) | -5 / 1 °C | Expert | |
| SkiGo | FFC Red | FFC Competition | Bloc (fer) | -5 / 1 °C | Expert | |
| SkiGo | FFC Blue | FFC Competition | Bloc (fer) | -10 / -3 °C | Expert | |
| SkiGo | FFC Green | FFC Competition | Bloc (fer) | -20 / -7 °C | Expert | |
| SkiGo | FFT Liquid (Fluor Free Training) | FFT Training | Liquide | -15 / 5 °C | Sport | |
| SkiGo | FFA Universal (Fluor Free Active) | FFA Active | Bloc (fer) | -15 / 5 °C | Debutant | |
| DragonSki | CH Medium | CH Entretien | Bloc (fer) | -8 / 2 °C | Debutant | |
| DragonSki | CH Cold | CH Entretien | Bloc (fer) | -15 / -5 °C | Debutant | |
| DragonSki | LSi Warm Jaune | LSi | Bloc (fer) | -1 / 10 °C | Sport | |
| DragonSki | LSi Medium Rouge | LSi | Bloc (fer) | -8 / 2 °C | Sport | |
| DragonSki | LSi Cold Bleu | LSi | Bloc (fer) | -15 / -5 °C | Sport | |
| DragonSki | LSi Warm Liquide | LSi | Liquide | -1 / 10 °C | Sport | |
| DragonSki | HSi Warm Liquide | HSi Performance | Liquide | -1 / 10 °C | Expert | |
| DragonSki | HSi Medium Liquide | HSi Performance | Liquide | -8 / 2 °C | Expert | |
| DragonSki | HSi Cold Liquide | HSi Performance | Liquide | -15 / -5 °C | Expert | |
| DragonSki | GT Warm | GT | Bloc (fer) | -4 / 10 °C | Expert | |
| DragonSki | GT SuperMED | GT | Bloc (fer) | -15 / -2 °C | Expert | |
| DragonSki | BP Base Preparation | BP | Bloc (fer) | -15 / 5 °C | Expert | |
| DragonSki | Cera S Warm | Cera S | Bloc (frottement) | -4 / 10 °C | Expert | |
| DragonSki | Cera S SuperMED | Cera S | Bloc (frottement) | -15 / -2 °C | Expert | |

## Validation

Le schéma JSON est validé automatiquement via GitHub Actions a chaque push ou pull request modifiant les fichiers du catalogue. Pour valider localement :

```bash
pip install check-jsonschema
check-jsonschema --schemafile glide_wax_schema.json glide_wax.json
```

## Licence

Les donnees de ce catalogue sont compilees a partir de sources publiques (sites fabricants, revendeurs). Voir le champ `metadata.sources` dans `glide_wax.json` pour la liste complete.
