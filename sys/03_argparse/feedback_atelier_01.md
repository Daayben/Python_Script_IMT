# Feedback — S03/A1 (Calculatrice CLI, BEN HAMOU Daniel)

> **Ré-évaluation à jour** : le dispatch utilise désormais `operator.add/sub/mul/truediv` (évaluation paresseuse de l'opération choisie), suivant la remarque précédente.

## Respect de la consigne

Critères attendus : mini-calculatrice CLI avec `argparse` — 3 positionnels (float, `choices=["+","-","*","/"]`, float), gestion de la division par zéro vers `stderr` + `exit(1)`.

Constat sur ton code :
- ✓ Trois positionnels : `a` (float), `op` (choices), `b` (float). Signature exactement conforme.
- ✓ `choices=["+", "-", "*", "/"]` → argparse rejette automatiquement les opérateurs invalides.
- ✓ Division par zéro : message d'erreur vers `sys.stderr` puis `sys.exit(1)`. Contrat respecté.
- ✓ Check de division par zéro fait **avant** le calcul (évite la `ZeroDivisionError` plutôt que de l'attraper).
- ✓ **Dispatch via `{"+": operator.add, ...}`** : seule l'opération choisie est effectivement appelée. La remarque précédente est intégrée.
- ✓ Format de sortie clair : `a op b = résultat`.

## Côté Python

- `import operator` : usage idiomatique des fonctions natives.
- Tout est dans `main()` avec garde — propre.

---
*Évalué sur le commit `6cb7630` (fichier `sys/03_argparse/atelier_01_Daniel_BENHAMOU.py`).*

---

## Évaluation précédente (obsolète, commit `092048c`)

# Feedback — Atelier 1 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : mini-calculatrice CLI avec `argparse` —
3 positionnels (float, `choices=["+","-","*","/"]`, float), gestion
de la division par zéro vers `stderr` + `exit(1)`.

Constat sur ton code :
- ✓ Trois positionnels : `a` (float), `op` (choices), `b` (float).
  Signature exactement conforme.
- ✓ `choices=["+", "-", "*", "/"]` → argparse rejette
  automatiquement les opérateurs invalides avec un message clair.
- ✓ Division par zéro : message d'erreur vers `sys.stderr` puis
  `sys.exit(1)`. Contrat respecté.
- ✓ Le check de division par zéro est fait **avant** le calcul,
  donc on évite la `ZeroDivisionError` plutôt que de l'attraper.
  Approche valide.
- ✓ Format de sortie clair : `a op b = résultat`.

## Côté Python

- Dispatch via un dict `{"+": a+b, ...}` plutôt qu'un `if/elif`.
  C'est élégant mais attention : **les quatre opérations sont
  toujours évaluées**, même celle qu'on ne garde pas. Ici sans
  impact, mais avec des opérations coûteuses ce serait un
  anti-pattern. Préférer un dict `{"+": operator.add, ...}` ou un
  `match`.
