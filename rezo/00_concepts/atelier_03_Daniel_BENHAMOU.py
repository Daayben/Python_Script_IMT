import argparse
import socket

CIBLE = ("127.0.0.1", 1)
TIMEOUT = 1


def tester_tcp():
    print(f"[TCP] Connexion à {CIBLE}...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect(CIBLE)
    except ConnectionRefusedError:
        print("  connexion refusée.")
    except TimeoutError:
        print("  timeout.")


def tester_udp():
    print(f"[UDP] Envoi vers {CIBLE}...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        n = s.sendto(b"bonjour", CIBLE)
        print(f"  {n} octet(s) envoyé(s), aucune confirmation possible.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocole", choices=["tcp", "udp"], required=True)
    args = parser.parse_args()

    if args.protocole == "tcp":
        tester_tcp()
    else:
        tester_udp()
