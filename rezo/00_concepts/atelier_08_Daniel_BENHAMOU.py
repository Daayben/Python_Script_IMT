import select
import socket
import time

# Pourquoi ne peut-on pas tester le mode bloquant pur ?
# recv() attendrait indéfiniment sans données → le script se fige.
# Il faudrait un thread émetteur pour débloquer le récepteur.

def mesurer(label: str, configurer, a: socket.socket, b: socket.socket):
    configurer(b)
    debut = time.perf_counter()
    try:
        b.recv(1)
    except (BlockingIOError, TimeoutError):
        pass
    duree = time.perf_counter() - debut
    print(f"{label} : {duree * 1000:.1f} ms")


def mesurer_select(a: socket.socket, b: socket.socket):
    debut = time.perf_counter()
    readable, _, _ = select.select([b], [], [], 0.2)
    duree = time.perf_counter() - debut
    print(f"select(timeout=0.2) : {duree * 1000:.1f} ms — lisible={bool(readable)}")


if __name__ == "__main__":
    a, b = socket.socketpair()
    with a, b:
        mesurer("settimeout(0.2)", lambda s: s.settimeout(0.2), a, b)

    a, b = socket.socketpair()
    with a, b:
        mesurer("setblocking(False)", lambda s: s.setblocking(False), a, b)

    a, b = socket.socketpair()
    with a, b:
        mesurer_select(a, b)
