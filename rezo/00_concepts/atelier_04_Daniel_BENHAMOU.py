import socket

# socketpair() retourne deux sockets déjà connectés.
# Sur Linux/macOS : famille AF_UNIX anonyme → adresses vides ('').
# Sur Windows (Python 3.12+) : AF_INET loopback → adresses ('127.0.0.1', port).
# Dans les deux cas les fileno() sont distincts : l'OS alloue un entier unique
# par descripteur ouvert.

def inspecter_paire():
    a, b = socket.socketpair()
    with a, b:
        for nom, s in [("Socket A", a), ("Socket B", b)]:
            print(f"{nom}")
            print(f"  fileno()     : {s.fileno()}")
            print(f"  getsockname(): {s.getsockname()!r}")
            print(f"  getpeername(): {s.getpeername()!r}")


if __name__ == "__main__":
    inspecter_paire()
