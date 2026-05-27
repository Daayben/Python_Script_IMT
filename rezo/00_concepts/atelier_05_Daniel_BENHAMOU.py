import socket


def recv_ligne(sock: socket.socket) -> bytes:
    """Lit octet par octet jusqu'à \\n, renvoie la ligne sans le délimiteur."""
    morceaux = []
    while True:
        octet = sock.recv(1)
        if not octet or octet == b"\n":
            break
        morceaux.append(octet)
    return b"".join(morceaux)

    # Inefficace en pratique : un appel système par octet.
    # Un buffer interne (bytearray) permettrait de lire par blocs
    # tout en consommant logiquement un octet à la fois.


if __name__ == "__main__":
    emetteur, recepteur = socket.socketpair()
    with emetteur, recepteur:
        emetteur.sendall(b"bonjour\nle monde\n")
        print(recv_ligne(recepteur))
        print(recv_ligne(recepteur))
