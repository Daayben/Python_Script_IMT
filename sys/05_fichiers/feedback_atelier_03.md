# Feedback — Atelier 3 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : journal horodaté — écrire des lignes
timestampées dans un fichier.

Constat sur ton code :
- ✓ Ouverture en mode `"a"` (append) : chaque appel ajoute une
  ligne, n'écrase pas l'historique.
- ✓ Horodatage via `datetime.datetime.now().isoformat(timespec="seconds")`
  → format ISO 8601 standard, tronqué à la seconde. Très propre.
- ✓ `encoding="utf-8"` explicite : évite les surprises Windows.
- ✓ `argparse` pour récupérer le message à journaliser plutôt que
  `sys.argv[1]` brut : aide automatique et message d'erreur clair.
- ✓ Format `<timestamp> <message>\n` lisible et grep-friendly.

## Côté Python

- Constante `LOG = "app.log"` en module : facile à modifier.
  Un `LOG = Path("app.log")` serait l'évolution naturelle, mais ce
  n'est pas requis ici.
- Fonction `journaliser(message)` pure et testable.

---
*Évalué sur le commit `092048c` (fichier `sys/05_fichiers/atelier_03_Daniel_BENHAMOU.py`).*
