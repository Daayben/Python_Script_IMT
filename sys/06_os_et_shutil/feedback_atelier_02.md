# Feedback — S06/A2 (Backup horodaté, BEN HAMOU Daniel)

> **Ré-évaluation à jour** : la variable `_` du genexp a été renommée en `p` (lisibilité accrue).

## Respect de la consigne

Critères attendus : backup horodaté — `shutil.copytree` vers `backup_<YYYYMMDD_HHMMSS>/`.

Constat sur ton code :
- ✓ `shutil.copytree(source, destination)` → copie récursive complète en un appel.
- ✓ Horodatage `datetime.now().strftime("%Y%m%d_%H%M%S")` : triable lexicographiquement, sans caractère problématique pour un nom de fichier.
- ✓ Destination calculée comme `source.parent / f"backup_{ts}"` : le backup atterrit à côté de la source, jamais dedans.
- ✓ Comptage des fichiers via `sum(1 for p in destination.rglob("*") if p.is_file())` — variable renommée `p`, conforme à la remarque précédente.
- ✓ `argparse` pour la CLI, fonction `backup(source: Path) -> Path` réutilisable et typée.

## Côté Python

- Type hint `-> Path` sur `backup` : bon réflexe documentaire.
- Une `FileExistsError` pourrait survenir si deux backups dans la même seconde — improbable mais non géré (note précédente toujours valable).

---
*Évalué sur le commit `6cb7630` (fichier `sys/06_os_et_shutil/atelier_02_Daniel_BENHAMOU.py`).*

---

## Évaluation précédente (obsolète, commit `092048c`)

# Feedback — Atelier 2 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : backup horodaté — `shutil.copytree` vers
`backup_<YYYYMMDD_HHMMSS>/`.

Constat sur ton code :
- ✓ `shutil.copytree(source, destination)` → copie récursive
  complète en un appel.
- ✓ Horodatage `datetime.now().strftime("%Y%m%d_%H%M%S")` :
  triable lexicographiquement, sans caractère problématique pour
  un nom de fichier.
- ✓ Destination calculée comme `source.parent / f"backup_{ts}"` :
  le backup atterrit à côté de la source, jamais dedans
  (sinon `copytree` boucle ou échoue selon les versions).
- ✓ Comptage des fichiers copiés via
  `sum(1 for _ in destination.rglob("*") if _.is_file())` —
  pattern correct.
- ✓ `argparse` pour la CLI, fonction `backup(source: Path)`
  réutilisable.

## Côté Python

- `_.is_file()` : le `_` est conventionnellement « variable
  ignorée ». Ici tu l'utilises tout de même comme `Path`. Pas
  faux, mais préfère un nom (`p` ou `chemin`) pour plus de
  clarté.
- Une `FileExistsError` pourrait survenir si deux backups dans la
  même seconde — improbable mais pas géré. Non bloquant.
