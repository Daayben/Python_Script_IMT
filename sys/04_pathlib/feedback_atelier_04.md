# Feedback — Atelier 4 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : `decomposer(chemin)` → `(parent, stem, suffix)`
via `pathlib.Path` ; trois exemples démontrant le cas `.tar.gz` et
le cas sans extension.

Constat sur ton code :
- ✓ Signature `decomposer(chemin: str) -> tuple[str, str, str]`
  avec annotation complète.
- ✓ Utilisation de `Path(chemin).parent / .stem / .suffix`.
  `str(p.parent)` pour rester sur des chaînes en sortie : cohérent
  avec l'annotation.
- ✓ Trois exemples bien choisis :
  - `/tmp/a.txt` → cas simple
  - `/var/log/archive.tar.gz` → met en évidence le piège
    classique (`.gz` seul, pas `.tar.gz`)
  - `/etc/hosts` → cas sans extension (`suffix = ""`)
- ✓ Affichage aligné avec `{c:<30}` : lecture facile.

## Côté Python

- Pour récupérer la double extension `.tar.gz`, l'idiome est
  `"".join(p.suffixes)`. Mais la consigne ne le demandait pas — le
  but de l'exemple était justement de **montrer** cette limitation.

---
*Évalué sur le commit `092048c` (fichier `sys/04_pathlib/atelier_04_Daniel_BENHAMOU.py`).*
