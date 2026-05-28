# Feedback — Atelier 7 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : lire le même paquet de 4 octets de trois
manières : big-endian, little-endian, octets inversés puis
big-endian.

Constat sur ton code :
- ✓ Trois lectures sur `b"\x00\x00\x00\x2A"` :
  `>I` (BE), `<I` (LE), `>I` sur `OCTETS[::-1]`. Spécificateurs
  `struct` corrects.
- ✓ **`assert little_endian == inverse_big`** : tu vérifies
  programmatiquement l'identité, ce n'était pas demandé mais c'est
  exactement le réflexe attendu.
- ✓ Explication finale en commentaire : « Lire en little-endian =
  lire en big-endian les octets inversés. » Formulation claire et
  juste.

## Côté Python

- Constantes en SCREAMING_SNAKE_CASE (`OCTETS`). Cohérent.
- Script linéaire sans fonction : acceptable pour un mini-exo de
  démonstration. Pas de `if __name__ == "__main__":` mais c'est
  sans conséquence ici.

---
*Évalué sur le commit `092048c` (fichier `rezo/00_concepts/atelier_07_Daniel_BENHAMOU.py`).*
