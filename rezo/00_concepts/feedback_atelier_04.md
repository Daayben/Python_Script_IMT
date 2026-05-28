# Feedback — Atelier 4 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : `getsockname()` / `getpeername()` sur une paire
client/serveur — montrer l'anatomie d'une connexion (4 endpoints).

Constat sur ton code :
- ✓ Utilisation de `socket.socketpair()` : élégant, évite un
  serveur d'écoute pour la démonstration.
- ✓ Affichage de `fileno()`, `getsockname()`, `getpeername()` pour
  chacune des deux sockets → 4 endpoints visibles.
- ✓ Commentaire de tête excellent : explique la différence
  Linux/macOS (`AF_UNIX` anonyme) vs Windows
  (`AF_INET` loopback). Ce niveau de précision portable est rare.
- ✓ Boucle `for nom, s in [...]` factorise proprement l'affichage.

## Côté Python

- Bloc `with a, b:` parenthésé idiomatique.
- `!r` dans les f-strings pour distinguer chaîne vide `''` de
  `None` ou de tuple. Très bon réflexe.

---
*Évalué sur le commit `092048c` (fichier `rezo/00_concepts/atelier_04_Daniel_BENHAMOU.py`).*
