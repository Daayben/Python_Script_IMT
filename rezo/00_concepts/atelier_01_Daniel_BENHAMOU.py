import socket
import argparse


def inspecter(nom):
    enregistrements = socket.getaddrinfo(nom, None)

    ipv4 = sorted({s[0] for f, *_, s in enregistrements if f == socket.AF_INET})
    ipv6 = sorted({s[0] for f, *_, s in enregistrements if f == socket.AF_INET6})

    print(f"Résolution de : {nom}")
    for adresse in ipv4:
        print(f"IPv4 : {adresse}")
    for adresse in ipv6:
        print(f"IPv6 : {adresse}")
    print(f"Total : {len(ipv4) + len(ipv6)} enregistrement(s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Inspecter les adresses IPv4 et IPv6 d'un nom de domaine"
    )
    parser.add_argument("nom", help="Nom de domaine à inspecter (ex: google.com)")
    args = parser.parse_args()
    inspecter(args.nom)
