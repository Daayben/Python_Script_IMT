# Feedback — Atelier 1 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : `getaddrinfo` + déduplication + format
`IPv4 : <adresse>` par ligne + comptage cohérent.

Constat sur ton code :
- ✓ `getaddrinfo` appelé une seule fois, résultat réutilisé pour
  IPv4 et IPv6.
- ✓ **Déduplication intégrée** via un set en compréhension :
  `sorted({s[0] for f, *_, s in enregistrements if ...})`. C'est
  exactement la correction attendue.
- ✓ Format de sortie ajusté : une ligne `IPv4 : <adresse>` par
  adresse, sans indentation.
- ✓ Total cohérent : `len(ipv4) + len(ipv6)` calculé après
  déduplication.
- ✓ Argparse plutôt que `sys.argv[1]` : l'aide est gratuite, et un
  appel sans argument produit un message clair au lieu d'un
  `IndexError`.

## Côté Python

- Dépaquetage idiomatique `f, *_, s` pour récupérer famille et
  sockaddr en ignorant les champs intermédiaires. Très propre.
- Pas de gestion de `socket.gaierror` : un domaine inexistant
  produira encore une trace brute. C'est acceptable mais reste le
  dernier point d'amélioration possible.

---
*Évalué sur le commit `092048c` (fichier `rezo/00_concepts/atelier_01_Daniel_BENHAMOU.py`).*

---

## Évaluation précédente (obsolète, commit `14b3307`)

# Feedback — Atelier 1 (Daniel BEN HAMOU)

## Respect de la consigne

L'argument CLI est lu, IPv4 et IPv6 sont séparées, le total est
imprimé. Le contrat de base est rempli.

Deux écarts :

- **Pas de déduplication** : tu construis `ipv4` et `ipv6` par
  compréhension de liste sur tous les enregistrements. Comme
  `getaddrinfo` retourne plusieurs tuples pour une même adresse (un
  par socket type : STREAM, DGRAM, RAW), tu auras des doublons.
  Tente sur `google.com` : tu verras `IPv4 : 142.x.y.z` plusieurs
  fois.
- **Total = `len(enregistrements)`** : tu comptes les tuples bruts
  (avec doublons). Si tu déduplique côté listes, le total doit
  reposer sur la même base : `len(ipv4) + len(ipv6)` (après dédup).

Format de sortie : tu indentes avec deux espaces sous la ligne
`Résolution de : nom`. C'est lisible, mais la consigne montre
plutôt une ligne par adresse non indentée (`IPv4 : ...`). Petit
détail.

## Côté réseau

- Les compréhensions de liste sont élégantes :
  ```python
  ipv4 = [s[0] for f, _, __, ___, s in enregistrements if f == socket.AF_INET]
  ```
  Bonne lecture du tuple par dépaquetage. Note : `_, __, ___` sont
  valides mais on peut écrire `_t, _p, _c` ou tout `_` (Python ne
  râle pas sur la collision dans ce contexte).
- Pour dédupliquer en gardant les compréhensions :
  ```python
  ipv4 = sorted({s[0] for f, *_, s in enregistrements if f == socket.AF_INET})
  ```
  Un set de compréhension + `sorted()` pour la reproductibilité.

## Côté Python (à titre indicatif)

- Structure propre : fonction `inspecter()` + garde
  `if __name__ == "__main__":`. Très bien.
- Pas de gestion de `socket.gaierror` ni de validation
  `len(sys.argv)` : un appel sans argument ou un domaine inexistant
  fera planter le script.
- Le nom de fichier inclut le nom de l'auteur
  (`atelier_01_Daniel_BENHAMOU.py`). Pour l'évaluation et la
  cohérence avec les autres rendus, je suggère `atelier_01.py` —
  l'auteur est de toute façon identifié par le dépôt git.

---
*Évalué sur le commit `14b3307` (fichier `atelier_01_Daniel_BENHAMOU.py`).*
