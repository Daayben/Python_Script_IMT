import socket
import sys


def inspecter(nom):
    enregistrements = socket.getaddrinfo(nom, None)

    ipv4 = [s[0] for f, _, __, ___, s in enregistrements if f == socket.AF_INET]
    ipv6 = [s[0] for f, _, __, ___, s in enregistrements if f == socket.AF_INET6]

    print(f"Résolution de : {nom}")
    for adresse in ipv4:
        print(f"  IPv4 : {adresse}")
    for adresse in ipv6:
        print(f"  IPv6 : {adresse}")
    print(f"Total : {len(enregistrements)} enregistrement(s)")


if __name__ == "__main__":
    inspecter(sys.argv[1])
