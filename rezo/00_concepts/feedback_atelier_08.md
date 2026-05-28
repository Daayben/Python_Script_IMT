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

---
*Évalué sur le commit `092048c` (fichier `rezo/00_concepts/atelier_08_Daniel_BENHAMOU.py`).*
