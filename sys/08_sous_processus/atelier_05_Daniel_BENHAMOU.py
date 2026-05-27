import subprocess
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage : python atelier_05.py <programme>", file=sys.stderr)
        sys.exit(2)

    nom = sys.argv[1]

    # which sur Unix/macOS, where sur Windows
    commande = "where" if sys.platform == "win32" else "which"

    try:
        resultat = subprocess.run(
            [commande, nom],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print(f"{commande} : introuvable dans le PATH", file=sys.stderr)
        sys.exit(2)

    if resultat.returncode == 0:
        chemin = resultat.stdout.strip().splitlines()[0]
        print(f"{nom} : {chemin}")
    else:
        print(f"{nom} : introuvable")
        sys.exit(1)


if __name__ == "__main__":
    main()
