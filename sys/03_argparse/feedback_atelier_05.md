# Feedback — Atelier 5 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : convertisseur de température avec `--from` /
`--to` (en passant par `dest=`), `choices=["C","F","K"]`, pivot
Celsius, format de précision configurable.

Constat sur ton code :
- ✓ `--from` / `--to` avec `dest="depuis"` / `dest="vers"` pour
  contourner le mot-clé réservé `from`. Exactement la technique
  attendue.
- ✓ Architecture pivot Celsius :
  `depuis_celsius(vers_celsius(valeur, depuis), vers)` —
  composition propre, évite la matrice 3×3 de conversions.
- ✓ `--precision` (défaut 2) → format dynamique
  `f".{args.precision}f"` injecté dans la f-string finale via
  `{val:{fmt}}`. Astucieux et idiomatique.
- ⚠ Les `choices` utilisent les noms longs (`celsius`, `fahrenheit`,
  `kelvin`) au lieu des lettres `C/F/K` mentionnées dans la
  consigne. Plus verbeux à la ligne de commande
  (`--from celsius`) mais plus lisible — choix défendable.

## Côté Python

- Annotations de types sur les helpers. Pas indispensable mais
  cohérent.
- Logique fonctionnelle (deux fonctions pures + composition) plutôt
  qu'une cascade de `if/elif`. Propre.

---
*Évalué sur le commit `092048c` (fichier `sys/03_argparse/atelier_05_Daniel_BENHAMOU.py`).*
