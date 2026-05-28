# Feedback — Atelier 2 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : phrase formatée à partir d'un prénom et d'un
âge ; gestion `ValueError` sur l'âge ; calcul de l'année de
naissance via `date.today().year`.

Constat sur ton code :
- ✓ Lecture du prénom et de l'âge via `input()`.
- ✓ Calcul `date.today().year - age` plutôt qu'une année codée en
  dur. Bon réflexe.
- ✓ Phrase formatée avec f-string : « Bonjour, X, tu as N ans, donc
  tu es né(e) vers ANNEE. »
- ⚠ **Pas de `try/except ValueError`** sur `int(input(...))` : un
  utilisateur qui tape « vingt » fera planter le script avec une
  trace Python. La consigne demandait explicitement ce garde-fou.

## Côté Python

- Garde `if __name__ == "__main__":` + fonction `main()` :
  structure propre.

---
*Évalué sur le commit `092048c` (fichier `sys/01_print_et_input/atelier_02_Daniel_BENHAMOU.py`).*
