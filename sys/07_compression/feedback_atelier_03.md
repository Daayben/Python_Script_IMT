# Feedback — Atelier 3 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : extraction sécurisée d'un `.tar.gz` — créer une
archive factice (via `tempfile`) + `tar.extractall(cible, filter="data")`
+ listage du résultat.

Constat sur ton code :
- ✓ **`filter="data"`** présent dans `extractall` : c'est le point
  critique de l'exo (mitigation CVE-2007-4559, recommandée depuis
  Python 3.12). Sans ce filtre, une archive malveillante peut
  écrire hors du dossier cible.
- ✓ Archive factice générée dans `tempfile.TemporaryDirectory()` :
  l'exo est entièrement self-contained et nettoyable.
- ✓ Cycle complet : création → écriture archive → extraction →
  relecture + affichage du contenu. Démo complète.
- ✓ Listage via `cible.rglob("*") if p.is_file()` + `sorted(...)` :
  ordre déterministe.
- ✓ `arcname=fichier.name` lors de `tar.add` : évite d'embarquer
  le chemin absolu temporaire dans l'archive.

## Côté Python

- Séparation `creer_archive` / `extraire_archive` : deux fonctions
  pures avec annotations. Très propre.
- Use de `Path.write_text(..., encoding="utf-8")` pour préparer
  les fichiers factices : idiomatique.

---
*Évalué sur le commit `092048c` (fichier `sys/07_compression/atelier_03_Daniel_BENHAMOU.py`).*
