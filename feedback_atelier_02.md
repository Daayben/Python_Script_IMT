# Feedback — Atelier 2 (Daniel BEN HAMOU)

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
