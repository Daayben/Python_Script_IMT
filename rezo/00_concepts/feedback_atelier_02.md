# Feedback — Atelier 2 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : trois sockets (TCP, UDP, AF_UNIX/STREAM) —
**AF_UNIX n'est plus exigé sous Windows**. Pour chaque socket :
`fileno()`, `family.name`, `type.name`. Question sur l'unicité des
`fileno()`.

Constat sur ton code :
- ✓ Deux sockets actifs (`AF_INET/STREAM`, `AF_INET/DGRAM`) +
  ligne `AF_UNIX` **conservée en commentaire** avec justification
  Windows. Tu montres que tu sais l'écrire — exactement ce qui
  était demandé après la mise à jour de la consigne.
- ✓ `fileno()`, `family.name`, `type.name` imprimés pour chacun.
- ✓ Vérification automatisée de l'unicité des `fileno()` :
  `len(filenos) == len(set(filenos))`.
- ✓ Réponse à la question, désormais reformulée correctement :
  « le plus petit entier libre de la table des descripteurs du
  processus » — c'est la règle POSIX exacte.
- ✓ Bloc `with` parenthésé unique au lieu de deux `with` imbriqués :
  c'est l'idiome moderne suggéré au feedback précédent.

## Côté Python

- Boucle `for nom, s in [("TCP", tcp), ("UDP", udp)]:` claire et
  scalable si tu décommentes le socket UNIX un jour.
- Commentaire de réponse placé après le bloc `with`. Lisible.

---
*Évalué sur le commit `092048c` (fichier `rezo/00_concepts/atelier_02_Daniel_BENHAMOU.py`).*

---

## Évaluation précédente (obsolète, commit `9c2da8c`)

# Feedback — Atelier 2 (Daniel BEN HAMOU)

> **Note du formateur (mise à jour 2026-05-27)** : la présence ou
> l'absence de `AF_UNIX` n'est **plus prise en compte** dans la
> notation. Plusieurs étudiants travaillent sous Windows où cette
> famille de sockets n'est pas (ou peu) supportée. Les remarques
> ci-dessous qui critiquaient l'absence ou le remplacement de
> `AF_UNIX` (par `AF_INET6` notamment) sont à considérer comme
> **caduques**.


## Respect de la consigne

Tu as deux sockets sur trois (`AF_INET/STREAM`, `AF_INET/DGRAM`) ;
le troisième `AF_UNIX/STREAM` est absent, justifié par le fait que
tu travailles sous Windows. Note légitime, mais alors le mieux est
de **garder le code AF_UNIX en commentaire** pour montrer que tu
sais l'écrire, comme l'a fait SERVOZ ou DUFRENEY. Ou de tester ton
script sous WSL/Linux.

- `fileno()`, `family.name`, `type.name` imprimés pour chacun ✓
- Bonne vérification automatisée :
  `len(filenos) == len(set(filenos))`. Élégant.
- Question répondue, et bien : « L'OS alloue un entier unique par
  ressource ouverte. » Tu pourrais préciser « le plus petit entier
  libre de la table des descripteurs du processus » — c'est cette
  règle qui explique la séquence 3, 4, 5.

## Côté Python (à titre indicatif)

- Tu utilises deux `with` imbriqués (un par ligne) au lieu d'un
  seul. Ça marche, mais l'idiome plus moderne est :
  ```python
  with (socket.socket(...) as tcp,
        socket.socket(...) as udp,
        socket.socket(...) as ux):
      ...
  ```
- Structure propre : `inspecter_sockets()` + garde
  `if __name__ == "__main__":`.

---
*Évalué sur le commit `9c2da8c` (fichier `atelier_02_Daniel_BENHAMOU.py`).*
