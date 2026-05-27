import socket


def inspecter_sockets():
    with (
        socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp,
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp,
        # socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as ux,  # Linux/macOS uniquement
    ):
        for nom, s in [("TCP", tcp), ("UDP", udp)]:
            print(nom)
            print("  fileno() :", s.fileno())
            print("  family   :", s.family.name)
            print("  type     :", s.type.name)
            print()

        filenos = [tcp.fileno(), udp.fileno()]
        print("Les fileno sont-ils tous différents ?", len(filenos) == len(set(filenos)))

    # Réponse : oui — l'OS alloue le plus petit entier libre de la table
    # des descripteurs du processus. Deux sockets ouverts simultanément
    # ne peuvent donc jamais partager le même fileno().


if __name__ == "__main__":
    inspecter_sockets()
