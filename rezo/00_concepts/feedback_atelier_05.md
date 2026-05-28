# Feedback — Atelier 5 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : implémenter `readline()` à la main sur une
socket (boucle `recv` jusqu'à `\n`).

Constat sur ton code :
- ✓ Boucle correcte : `recv(1)` octet par octet, arrêt sur `\n` ou
  fermeture (`not octet`).
- ✓ Le délimiteur n'est pas inclus dans le retour, comme convenu.
- ✓ Démo claire avec `socketpair()` + deux lignes envoyées :
  `b"bonjour"` puis `b"le monde"` lues correctement.
- ✓ Bonus pédagogique : le commentaire final reconnaît que lire
  octet par octet est inefficace (un syscall par octet) et évoque
  l'amélioration possible avec un tampon interne. Très bon
  réflexe.

## Côté Python

- `morceaux = []` + `b"".join(morceaux)` : pattern idiomatique pour
  éviter les concaténations quadratiques.
- Annotation de type `sock: socket.socket -> bytes` + docstring
  courte. Très propre.

---
*Évalué sur le commit `092048c` (fichier `rezo/00_concepts/atelier_05_Daniel_BENHAMOU.py`).*
