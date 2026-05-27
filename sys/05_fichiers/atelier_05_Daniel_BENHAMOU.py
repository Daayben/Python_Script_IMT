import argparse
import re
import collections


def compter_occurrences(chemin: str, mot: str) -> int:
    mot = mot.lower()
    compteur = 0
    with open(chemin, encoding="utf-8", errors="replace") as f:
        for ligne in f:
            mots = re.findall(r"\w+", ligne.lower())
            compteur += collections.Counter(mots)[mot]
    return compteur


def main():
    parser = argparse.ArgumentParser(
        description="Compter les occurrences d'un mot dans un fichier"
    )
    parser.add_argument("fichier", help="Chemin du fichier texte")
    parser.add_argument("mot", help="Mot à chercher (insensible à la casse)")
    args = parser.parse_args()

    n = compter_occurrences(args.fichier, args.mot)
    print(f"Le mot '{args.mot}' apparait {n} fois.")


if __name__ == "__main__":
    main()
