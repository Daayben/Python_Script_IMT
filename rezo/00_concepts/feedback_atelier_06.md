# Feedback — Atelier 6 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : protocole à préfixe de longueur (4 octets
big-endian) — fonctions `envoyer` / `recevoir`.

Constat sur ton code :
- ✓ Préfixe 4 octets big-endian via `struct.pack("!I", ...)` —
  exactement la convention attendue (`!` = network order).
- ✓ `envoyer_message` colle préfixe + payload et envoie en un seul
  `sendall`.
- ✓ `recevoir_message` lit d'abord 4 octets, décode la longueur,
  puis lit exactement N octets.
- ✓ Helper `_recv_exactement` (souligné = privé) qui gère le cas
  où `recv` rend moins que demandé. Cas limite (`not morceau` →
  `ConnectionError`) traité proprement.
- ✓ Démo avec trois messages de longueurs différentes + `assert`
  pour valider le round-trip. Test intégré.

## Côté Python

- Annotations de types partout, helper privé, exception métier
  explicite : niveau prod.
- `len(tampon) < n` avec accumulation par `tampon += morceau` :
  petit détail, on pourrait utiliser `bytearray` + `extend` pour
  éviter la création de bytes intermédiaires, mais sur 4-N octets
  c'est sans impact.

---
*Évalué sur le commit `092048c` (fichier `rezo/00_concepts/atelier_06_Daniel_BENHAMOU.py`).*
