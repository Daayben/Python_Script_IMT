import sys
from datetime import date


def main():
    prenom = input("Ton prénom : ")
    try:
        age = int(input("Ton âge : "))
    except ValueError:
        print("Erreur : l'âge doit être un entier.", file=sys.stderr)
        sys.exit(1)
    annee_naissance = date.today().year - age
    print(f"Bonjour, {prenom}, tu as {age} ans, donc tu es né(e) vers {annee_naissance}.")


if __name__ == "__main__":
    main()
