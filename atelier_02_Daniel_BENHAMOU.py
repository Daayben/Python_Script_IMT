import socket


def inspecter_sockets():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:

            for nom, s in [("TCP", tcp), ("UDP", udp)]:
                print(nom)
                print("  fileno() :", s.fileno())
                print("  family   :", s.family.name)
                print("  type     :", s.type.name)
                print()

            filenos = [tcp.fileno(), udp.fileno()]
            print("Les fileno sont-ils tous différents ?", len(filenos) == len(set(filenos)))


if __name__ == "__main__":
    inspecter_sockets()

# Réponse : Oui, les fileno() sont nécessairement différents.
# L'OS alloue un entier unique par ressource ouverte.
# Deux sockets ouverts simultanément ne peuvent pas partager le même descripteur.
# Note : AF_UNIX non testé car je suis sous Windows.
