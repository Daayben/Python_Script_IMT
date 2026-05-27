import socket
import struct


def envoyer_message(sock: socket.socket, message: bytes) -> None:
    sock.sendall(struct.pack("!I", len(message)) + message)


def recevoir_message(sock: socket.socket) -> bytes:
    longueur = struct.unpack("!I", _recv_exactement(sock, 4))[0]
    return _recv_exactement(sock, longueur)


def _recv_exactement(sock: socket.socket, n: int) -> bytes:
    tampon = b""
    while len(tampon) < n:
        morceau = sock.recv(n - len(tampon))
        if not morceau:
            raise ConnectionError("connexion fermée avant la fin du message")
        tampon += morceau
    return tampon


if __name__ == "__main__":
    messages = [b"a", b"bb", b"ccc"]

    emetteur, recepteur = socket.socketpair()
    with emetteur, recepteur:
        for m in messages:
            envoyer_message(emetteur, m)
        for m in messages:
            recu = recevoir_message(recepteur)
            assert recu == m, f"attendu {m!r}, reçu {recu!r}"
            print(f"OK : {recu!r}")
