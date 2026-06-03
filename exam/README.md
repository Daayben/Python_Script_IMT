# Annuaire de domaines

Mini-annuaire de domaines accessible en réseau. Pour chaque nom d'hôte, l'application
collecte et enregistre quatre informations :

- l'adresse **IP** résolue ;
- le **nom d'hôte** (clé primaire) ;
- le **contact** déclaré dans le `whois` ;
- l'**email** déclaré dans le `whois`.

L'application est livrée comme un **script unique** (`annuaire.py`) lançable en deux modes
— serveur ou client — via une CLI commune.

## Architecture

```
CLI (argparse)
   ├── serve ─────────────► Serveur (socketserver, threadé)
   └── search/record/...──► Client (sockets bas niveau)
                                   │
                                   ▼
                         Couche données (SQLAlchemy + Pydantic)
                                   │
                                   ▼
                         Collecte système (subprocess : nslookup / whois)
```

| Partie | Module | Rôle |
|--------|--------|------|
| 1 | Collecte | `resoudre_ip`, `interroger_whois`, `collecter` → modèle `Domaine` (Pydantic) |
| 2 | Persistance | `enregistrer`, `lister`, `chercher` (SQLite via SQLAlchemy, ORM interne) |
| 3 | Serveur | `socketserver.ThreadingMixIn` + `TCPServer`, arrêt propre sur Ctrl-C |
| 4 | Client | `socket` bas niveau, framing manuel (`recv_ligne`), gestion des timeouts |
| 5 | CLI | sous-commandes `argparse`, logging à niveaux de verbosité |

## Installation

```bash
# Dépendances Python
pip install -r requirements.txt

# Outil whois (Linux/Debian)
sudo apt install whois
```

> Sous **Windows**, la résolution IP utilise `nslookup` (présent par défaut). `whois`
> n'est pas livré avec Windows : le contact/email seront `None` si l'outil est absent,
> ce qui est géré proprement (aucune erreur).

## Configuration

L'adresse d'écoute (`HOST`) et le port (`PORT`) sont lus depuis un fichier `.env`
(via `python-dotenv`). Valeurs par défaut : `127.0.0.1:8888`.

```bash
cp .env.example .env   # puis ajuster si besoin
```

## Usage

### Serveur

```bash
python annuaire.py serve
python annuaire.py serve --host 0.0.0.0 --port 9000
```

### Client

```bash
python annuaire.py record google.com   # résout IP + whois, puis enregistre
python annuaire.py search google.com   # recherche en base
python annuaire.py count               # nombre d'enregistrements
python annuaire.py list                # liste des hôtes
```

### Verbosité (logging)

| Flag | Niveau | Usage |
|------|--------|-------|
| *(aucun)* | `WARNING` | erreurs uniquement |
| `-v` | `INFO` | commandes reçues, résultats |
| `-vv` | `DEBUG` | détails (parsing whois, framing) |
| `-vvv` | `DEBUG` | format détaillé (timestamp, thread, fichier:ligne) |

```bash
python annuaire.py -vv serve
```

## Protocole

**Protocole A — texte ligne** (`\n` comme délimiteur).

> Choisi car lisible humainement et testable directement avec `netcat`, cohérent avec
> les cours R00/A sur les sockets bas niveau. Le payload étant du texte UTF-8 uniquement,
> l'absence de binary-safety n'est pas un problème dans ce contexte.

| Commande | Réponse |
|----------|---------|
| `SEARCH <hote>` | `OK hote=... ip=... contact=... email=...` ou `NOT_FOUND` |
| `RECORD <hote>` | `OK` / `ALREADY EXISTS.` / `ERROR <message>` |
| `COUNT` | entier en texte |
| `LIST` | un hôte par ligne, terminé par une ligne `.` |

### Tester le serveur avec netcat

```bash
nc 127.0.0.1 8888
COUNT
RECORD python.org
SEARCH python.org
LIST
```

## Tests

```bash
python -m pytest tests/ -v
```

Les tests couvrent la couche données (insertion, doublon, liste, recherche) sur une base
SQLite temporaire isolée.
