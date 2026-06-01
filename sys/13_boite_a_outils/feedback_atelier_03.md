# Feedback — S13/A3 (Token URL-safe, BEN HAMOU Daniel)

> **Ré-évaluation à jour** : structure inchangée, code propre, déjà conforme. Pas d'évolution notable à signaler.

## Respect de la consigne

Critères attendus : générer un token URL-safe avec `secrets.token_urlsafe(32)`, l'écrire dans un `.env` temporaire, le relire, comparer avec `secrets.compare_digest`.

Constat sur ton code :
- ✓ `secrets.token_urlsafe(32)` : la bonne API.
- ✓ Écriture dans un `.env` à l'intérieur d'un `tempfile.TemporaryDirectory()` : auto-nettoyage à la sortie du `with`.
- ✓ Chemin construit avec `Path(tmpdir) / ".env"` (cohérence pathlib).
- ✓ Relecture, extraction de la valeur via `contenu.partition("=")` : robuste.
- ✓ **`secrets.compare_digest(token, valeur)`** : comparaison en temps constant, critère central rempli.
- ✓ Affichage des quatre infos (chemin, contenu brut, valeur lue, résultat de la comparaison).

## Côté Python

- `with open(..., encoding="utf-8")` partout : bon réflexe.

---
*Évalué sur le commit `6cb7630` (fichier `sys/13_boite_a_outils/atelier_03_Daniel_BENHAMOU.py`).*

---

## Évaluation précédente (obsolète, commit `8975ae0`)

# Feedback — Atelier 3 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : générer un token URL-safe avec
`secrets.token_urlsafe(32)`, l'écrire dans un `.env` temporaire,
le relire, comparer avec `secrets.compare_digest`.

Constat sur ton code :
- ✓ `secrets.token_urlsafe(32)` : la bonne API (et non
  `random` ou `os.urandom` reformaté).
- ✓ Écriture dans un `.env` à l'intérieur d'un
  `tempfile.TemporaryDirectory()` : auto-nettoyage à la sortie du
  `with`.
- ✓ Relecture, extraction de la valeur via
  `contenu.partition("=")` : robuste même si la valeur contient
  des `=` (token URL-safe n'en contient pas, mais le réflexe est
  bon).
- ✓ **`secrets.compare_digest(token, valeur)`** : comparaison en
  temps constant, exactement ce qui est attendu pour des
  secrets (évite les attaques par timing). Le critère central de
  l'atelier est rempli.
- ✓ Affichage des trois infos (chemin, contenu brut, valeur lue,
  résultat de la comparaison).

## Côté Python

- `with open(..., encoding="utf-8")` partout : bon réflexe.
- Mélange `os.path.join` + `tempfile` : pourrait être unifié avec
  `Path(tmpdir) / ".env"`, mais c'est cosmétique.
