# Feedback — R00/A8 (Deux modes d'attente, BEN HAMOU Daniel)

> **Ré-évaluation à jour** : ajout d'une troisième mesure avec `select.select(timeout=0.2)` pour compléter la comparaison demandée par la consigne.

## Respect de la consigne

Critères attendus : comparer `socket.timeout` (via `settimeout`) et `select.select()` pour mesurer l'attente d'un `recv` sur un socket sans données.

Constat sur ton code :
- ✓ Mesure avec `time.perf_counter()` (haute précision).
- ✓ Trois scénarios mesurés en ms : `settimeout(0.2)` (~200 ms), `setblocking(False)` (~0 ms via `BlockingIOError`), et `select.select([b],[],[],0.2)` (~200 ms, lisible=False).
- ✓ Fonction `mesurer_select` séparée, sortie indiquant clairement la valeur de `bool(readable)`.
- ✓ Trois `socketpair` distinctes — pas de contamination entre tests.
- ✓ Exceptions correctement attrapées : `BlockingIOError` (non bloquant) et `TimeoutError` (timeout).
- ✓ Commentaire d'introduction expliquant pourquoi le mode bloquant pur n'est pas testable sans thread émetteur. Bonne conscience des limites.
- ✓ Le reproche précédent (absence de `select`) est corrigé.

## Côté Python

- Helper `mesurer(label, configurer, a, b)` factorise via lambda de configuration. Élégant.
- `mesurer_select` reste séparée (signature différente). Acceptable mais on pourrait imaginer unifier.

---
*Évalué sur le commit `6cb7630` (fichier `rezo/00_concepts/atelier_08_Daniel_BENHAMOU.py`).*

---

## Évaluation précédente (obsolète, commit `092048c`)

# Feedback — Atelier 8 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : mesurer le temps d'attente d'un `recv` avec
`socket.timeout` (via `settimeout`) et avec `setblocking(False)`,
comparer.

Constat sur ton code :
- ✓ Mesure avec `time.perf_counter()` (et non `time.time()`) →
  bonne précision.
- ✓ Deux scénarios mesurés et imprimés en ms :
  `settimeout(0.2)` (~200 ms) vs `setblocking(False)` (~0 ms via
  `BlockingIOError`).
- ✓ Exceptions correctement attrapées : `BlockingIOError` pour le
  mode non bloquant, `TimeoutError` pour le timeout (sous-classe
  de `OSError`, alias historique de `socket.timeout`).
- ✓ Bonus : le commentaire de tête explique pourquoi le mode
  bloquant pur n'est pas testable sans un thread émetteur. Bonne
  conscience des limites de l'exo.
- ⚠ La consigne mentionnait aussi `select.select()` comme troisième
  comparaison. Tu n'as gardé que `timeout` vs non-bloquant — c'est
  l'essentiel, mais un `select` rapide aurait complété le tableau.

## Côté Python

- Helper `mesurer(label, configurer, a, b)` factorise les deux
  essais avec une lambda de configuration. Pattern élégant.
- Deux paires `socketpair` distinctes pour éviter qu'un test
  contamine l'autre. Bon réflexe.
