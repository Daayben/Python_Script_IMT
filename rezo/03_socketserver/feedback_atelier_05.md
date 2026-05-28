# Feedback — Atelier 5 (Daniel BEN HAMOU)

## Respect de la consigne

Critères attendus : `ThreadingMixIn` combiné à `TCPServer` (mixin
en **premier** dans l'héritage), avec un `time.sleep` dans le
handler pour rendre le parallélisme visible.

Constat sur ton code :
- ✓ `class ServeurMultiClient(socketserver.ThreadingMixIn, socketserver.TCPServer)`
  → ordre des bases **correct** (`ThreadingMixIn` d'abord, c'est
  l'erreur la plus fréquente).
- ✓ `time.sleep(2)` au début du `handle` → deux clients simultanés
  observeront bien des `[connexion]` en parallèle.
- ✓ `StreamRequestHandler` + `self.rfile.readline()` / `self.wfile.write(...)`
  : utilisation idiomatique du wrapper fichier-like.
- ✓ `allow_reuse_address = True` : permet de relancer le serveur
  sans attendre `TIME_WAIT`.
- ✓ Boucle `while ligne := self.rfile.readline()` (déguisée sous
  `if not ligne: break`) pour gérer la fermeture côté client.
- ✓ Logs `[connexion]` / `[deconnexion]` avec l'adresse, et
  bannière de démarrage avec `HOST:PORT` + rappel `Ctrl+C`.

## Côté Python

- Usage du gestionnaire de contexte `with ServeurMultiClient(...) as serveur`
  : propre, ferme le socket d'écoute à la sortie.

---
*Évalué sur le commit `092048c` (fichier `rezo/03_socketserver/atelier_05_Daniel_BENHAMOU.py`).*
