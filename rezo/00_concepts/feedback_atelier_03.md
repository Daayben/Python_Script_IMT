# Feedback — Atelier 3 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : choisir TCP ou UDP et écrire un petit script
client/serveur démonstratif des différences.

Constat sur ton code :
- ✓ Tu démontres les **deux** protocoles côté client : connexion
  TCP qui échoue proprement vs envoi UDP sans confirmation. C'est
  une approche pédagogique très claire.
- ✓ La cible `("127.0.0.1", 1)` (port réservé) garantit l'échec
  TCP : `ConnectionRefusedError` ou `TimeoutError`, gérés tous les
  deux.
- ✓ Le contraste fire-and-forget est explicite : `sendto` réussit
  silencieusement, le commentaire « aucune confirmation possible »
  appuie la leçon.
- ⚠ Pas de petit serveur côté script (on observe surtout le client) :
  l'esprit de la consigne était plutôt un mini échange. Cela dit, ta
  démo des comportements asymétriques fixe parfaitement la différence
  TCP/UDP, donc c'est acceptable.

## Côté Python

- `argparse` avec `choices=["tcp","udp"]` + `required=True` : très
  propre.
- Timeout court (1 s) sur TCP pour ne pas bloquer.

---
*Évalué sur le commit `092048c` (fichier `rezo/00_concepts/atelier_03_Daniel_BENHAMOU.py`).*
