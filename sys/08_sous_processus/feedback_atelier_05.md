# Feedback — Atelier 5 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : mini `which` — `subprocess.run(["which", nom])`,
gestion du code retour 0/!0 et de `FileNotFoundError` si la
commande `which` est absente.

Constat sur ton code :
- ✓ `subprocess.run` avec `capture_output=True, text=True` :
  idiomatique pour récupérer stdout en chaîne.
- ✓ Branchement portable Unix/Windows :
  `"where" if sys.platform == "win32" else "which"`. Bonus
  par rapport à la consigne, et pertinent.
- ✓ Gestion des trois cas :
  - `returncode == 0` → affiche le chemin trouvé
  - `returncode != 0` → message « introuvable » + `exit(1)`
  - `FileNotFoundError` (la commande `which/where` n'existe pas) →
    message dédié + `exit(2)`
- ✓ Codes de sortie distincts (1 vs 2) : utile pour distinguer
  « programme introuvable » de « outil système manquant ».
- ✓ Validation de `len(sys.argv)` avec usage + `exit(2)`.
- ✓ `resultat.stdout.strip().splitlines()[0]` : robuste face à
  `where` (Windows) qui peut renvoyer plusieurs lignes.

## Côté Python

- Pas de `check=True` sur `subprocess.run` : volontaire ici car tu
  analyses toi-même le `returncode`. Correct.

---
*Évalué sur le commit `3746a69` (fichier `sys/08_sous_processus/atelier_05_Daniel_BENHAMOU.py`).*
