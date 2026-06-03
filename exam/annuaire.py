"""
annuaire.py — Mini-annuaire de domaines accessible en réseau.

Protocole A choisi (texte ligne, \\n comme délimiteur).
Lisible humainement et testable directement avec netcat,
cohérent avec les cours R00/A sur les sockets bas niveau.
Le payload étant du texte UTF-8 uniquement, l'absence de
binary-safety n'est pas un problème dans ce contexte.
"""

import argparse
import logging
import os
import platform
import re
import socket
import socketserver
import subprocess
import sys
from pathlib import Path

from pydantic import BaseModel, EmailStr, ValidationError
from sqlalchemy import Column, String, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Session

# Configuration via .env si python-dotenv est dispo (bonus 5.3)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8888"))

logger = logging.getLogger(__name__)


# Partie 1 — Collecte d'informations

def resoudre_ip(hote: str) -> str | None:
    """
    Résout l'IPv4 de hote via nslookup (cross-platform), avec un repli sur
    host sous Linux/macOS. Retourne None si la résolution échoue (timeout,
    code retour non nul, outil absent).
    """
    systeme = platform.system()
    commandes = [["nslookup", hote]]
    if systeme in ("Linux", "Darwin"):
        commandes.append(["host", hote])

    for commande in commandes:
        try:
            res = subprocess.run(commande, capture_output=True, text=True, timeout=5.0)
            if res.returncode != 0:
                continue
            if commande[0] == "nslookup":
                # la première Address est celle du serveur DNS, on veut la dernière
                adresses = re.findall(
                    r"Address:\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", res.stdout
                )
                if adresses:
                    return adresses[-1]
            else:
                m = re.search(r"has address (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", res.stdout)
                if m:
                    return m.group(1)
        except FileNotFoundError:
            logger.debug("outil %s introuvable", commande[0])
        except subprocess.TimeoutExpired:
            logger.debug("timeout %s pour %s", commande[0], hote)

    return None


def interroger_whois(hote: str) -> tuple[str | None, str | None]:
    """
    Interroge whois et retourne (contact, email). Le format whois varie selon
    le TLD, d'où les deux motifs pour le contact. Retourne (None, None) si
    whois est absent, échoue ou expire.
    """
    try:
        res = subprocess.run(["whois", hote], capture_output=True, text=True, timeout=10.0)
        if res.returncode != 0:
            return None, None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None, None

    contact = None
    m = re.search(r"Registrant Name:?\s+(.+)", res.stdout, re.IGNORECASE)
    if not m:
        m = re.search(r"Registrant:\s+(.+)", res.stdout, re.IGNORECASE)
    if m:
        contact = m.group(1).strip()

    email = None
    m = re.search(r"(\S+@\S+)", res.stdout)
    if m:
        email = m.group(1).rstrip(".,;)")
        if "@" not in email:
            email = None

    return contact, email


class Domaine(BaseModel):
    """
    Enregistrement de l'annuaire (validation Pydantic, email vérifié nativement).

    >>> d = Domaine(hote="example.com", ip="93.184.216.34", contact=None, email=None)
    >>> d.hote
    'example.com'
    """

    hote: str
    ip: str | None
    contact: str | None
    email: EmailStr | None


def collecter(hote: str) -> Domaine:
    """
    Combine la résolution IP (1.1) et le whois (1.2) en un Domaine.

    Si l'email extrait du whois n'est pas valide, on le met à None plutôt que
    de laisser la validation Pydantic faire échouer toute la collecte.
    """
    ip = resoudre_ip(hote)
    contact, email = interroger_whois(hote)
    try:
        return Domaine(hote=hote, ip=ip, contact=contact, email=email)
    except ValidationError:
        return Domaine(hote=hote, ip=ip, contact=contact, email=None)


# Partie 2 — Persistance SQLAlchemy

class Base(DeclarativeBase):
    pass


class DomaineORM(Base):
    """Modèle ORM, table domaines. Reste interne à la couche données."""

    __tablename__ = "domaines"
    hote = Column(String, primary_key=True)
    ip = Column(String)
    contact = Column(String)
    email = Column(String)


BDD_PATH = Path(__file__).parent / "domaines.db"
engine = create_engine(f"sqlite:///{BDD_PATH}")
Base.metadata.create_all(engine)


def _orm_vers_pydantic(d: DomaineORM) -> Domaine:
    """Convertit une ligne ORM en Domaine Pydantic (email douteux -> None)."""
    try:
        return Domaine(hote=d.hote, ip=d.ip, contact=d.contact, email=d.email)
    except ValidationError:
        return Domaine(hote=d.hote, ip=d.ip, contact=d.contact, email=None)


def enregistrer(domaine: Domaine) -> None:
    """Insère domaine en base. Lève ValueError si l'hôte est déjà présent."""
    with Session(engine) as session:
        try:
            session.add(DomaineORM(**domaine.model_dump()))
            session.commit()
        except IntegrityError:
            raise ValueError(f"{domaine.hote} déjà enregistré")


def lister() -> list[Domaine]:
    """Retourne tous les enregistrements sous forme de Domaine."""
    with Session(engine) as session:
        return [_orm_vers_pydantic(d) for d in session.query(DomaineORM).all()]


def chercher(hote: str) -> Domaine | None:
    """
    Recherche un domaine par sa clé primaire, ou None s'il n'existe pas.

    >>> chercher("hote-qui-nexiste-pas.invalid") is None
    True
    """
    with Session(engine) as session:
        d = session.get(DomaineORM, hote)
        return _orm_vers_pydantic(d) if d else None


# Partie 3 — Serveur d'application

def _traiter(ligne: str) -> str:
    """
    Exécute une commande du protocole et renvoie la réponse texte.
    LIST renvoie un hôte par ligne, terminé par une ligne '.'.
    """
    parts = ligne.strip().split(maxsplit=1)
    if not parts:
        return "ERR commande vide"

    cmd = parts[0].upper()
    arg = parts[1] if len(parts) > 1 else ""

    if cmd == "SEARCH":
        if not arg:
            return "ERR usage: SEARCH <hote>"
        d = chercher(arg)
        if d is None:
            return "NOT_FOUND"
        return f"OK hote={d.hote} ip={d.ip} contact={d.contact!r} email={d.email!r}"

    if cmd == "RECORD":
        if not arg:
            return "ERR usage: RECORD <hote>"
        if chercher(arg) is not None:
            return "ALREADY EXISTS."
        try:
            enregistrer(collecter(arg))
            return "OK"
        except Exception as exc:
            logger.exception("RECORD %s a échoué", arg)
            return f"ERROR {exc}"

    if cmd == "COUNT":
        with Session(engine) as session:
            return str(session.query(DomaineORM).count())

    if cmd == "LIST":
        lignes = [d.hote for d in lister()] + ["."]
        return "\n".join(lignes)

    return f"ERR commande inconnue: {cmd}"


class _Handler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        logger.info("connexion de %s:%s", *self.client_address)
        for raw in self.rfile:
            ligne = raw.decode("utf-8").strip()
            if not ligne:
                continue
            logger.debug("← %s", ligne)
            reponse = _traiter(ligne)
            logger.debug("→ %s", reponse)
            self.wfile.write((reponse + "\n").encode("utf-8"))
            self.wfile.flush()
        logger.info("déconnexion de %s:%s", *self.client_address)


class _Serveur(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def demarrer_serveur(host: str, port: int) -> None:
    """Lance le serveur TCP et bloque jusqu'à Ctrl-C."""
    with _Serveur((host, port), _Handler) as srv:
        logger.warning("serveur démarré sur %s:%d  (Ctrl-C pour arrêter)", host, port)
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            logger.warning("arrêt du serveur")


# Partie 4 — Client réseau

def recv_ligne(sock: socket.socket) -> str:
    """Lit une ligne octet par octet jusqu'au \\n (framing manuel, protocole A)."""
    buf = b""
    while not buf.endswith(b"\n"):
        octet = sock.recv(1)
        if not octet:
            break
        buf += octet
    return buf.decode("utf-8").strip()


def _envoyer(sock: socket.socket, commande: str) -> str:
    sock.sendall((commande + "\n").encode("utf-8"))
    return recv_ligne(sock)


def cmd_search(sock: socket.socket, hote: str) -> Domaine | None:
    """Envoie SEARCH et reconstruit un Domaine, ou None si NOT_FOUND."""
    reponse = _envoyer(sock, f"SEARCH {hote}")
    if reponse == "NOT_FOUND":
        return None
    m_ip = re.search(r"ip=(\S+)", reponse)
    m_contact = re.search(r"contact='([^']*)'", reponse)
    m_email = re.search(r"email='([^']*)'", reponse)
    ip = m_ip.group(1) if m_ip else None
    # le serveur sérialise None tel quel : on retraduit la sentinelle
    if ip == "None":
        ip = None
    try:
        return Domaine(
            hote=hote,
            ip=ip,
            contact=m_contact.group(1) if m_contact else None,
            email=m_email.group(1) if m_email else None,
        )
    except ValidationError:
        return Domaine(hote=hote, ip=ip, contact=None, email=None)


def cmd_record(sock: socket.socket, hote: str) -> str:
    """Envoie RECORD et retourne 'OK', 'ALREADY EXISTS.' ou 'ERROR ...'."""
    return _envoyer(sock, f"RECORD {hote}")


def cmd_count(sock: socket.socket) -> int:
    """Envoie COUNT et retourne le nombre d'enregistrements."""
    return int(_envoyer(sock, "COUNT"))


def cmd_list(sock: socket.socket) -> list[str]:
    """Envoie LIST et retourne la liste des hôtes (lecture jusqu'au '.')."""
    sock.sendall(b"LIST\n")
    hotes = []
    while True:
        ligne = recv_ligne(sock)
        if ligne == ".":
            break
        if ligne:
            hotes.append(ligne)
    return hotes


# Partie 5 — Interface CLI

def _configurer_logging(verbosity: int) -> None:
    niveaux = [logging.WARNING, logging.INFO, logging.DEBUG]
    niveau = niveaux[min(verbosity, 2)]
    if verbosity >= 3:
        fmt = "%(asctime)s %(threadName)s %(filename)s:%(lineno)d %(levelname)s %(message)s"
    else:
        fmt = "%(levelname)s %(message)s"
    logging.basicConfig(level=niveau, format=fmt, stream=sys.stderr)


def construire_parser() -> argparse.ArgumentParser:
    """Construit le parser CLI avec les sous-commandes serve/search/record/count/list."""
    p = argparse.ArgumentParser(
        prog="annuaire.py",
        description="Mini-annuaire de domaines accessible en réseau.",
    )
    p.add_argument("-v", "--verbose", action="count", default=0,
                   help="-v INFO  -vv DEBUG  -vvv DEBUG détaillé")

    sub = p.add_subparsers(dest="commande", required=True)

    srv = sub.add_parser("serve", help="Lance le serveur")
    srv.add_argument("--host", default=HOST)
    srv.add_argument("--port", type=int, default=PORT)

    for nom in ("search", "record", "count", "list"):
        sp = sub.add_parser(nom)
        sp.add_argument("--host", default=HOST)
        sp.add_argument("--port", type=int, default=PORT)
        if nom in ("search", "record"):
            sp.add_argument("hote")

    return p


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée : lance le serveur ou envoie une commande au serveur."""
    args = construire_parser().parse_args(argv)
    _configurer_logging(args.verbose)

    if args.commande == "serve":
        demarrer_serveur(args.host, args.port)
        return 0

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10.0)
            s.connect((args.host, args.port))

            if args.commande == "search":
                d = cmd_search(s, args.hote)
                print(d if d else "NOT_FOUND")
            elif args.commande == "record":
                print(cmd_record(s, args.hote))
            elif args.commande == "count":
                print(cmd_count(s))
            elif args.commande == "list":
                hotes = cmd_list(s)
                print("\n".join(hotes) if hotes else "(aucun)")

    except ConnectionRefusedError:
        logger.error("connexion refusée sur %s:%d", args.host, args.port)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
