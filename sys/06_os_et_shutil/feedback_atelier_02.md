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

---
*Évalué sur le commit `092048c` (fichier `sys/06_os_et_shutil/atelier_02_Daniel_BENHAMOU.py`).*
