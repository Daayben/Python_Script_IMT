from datetime import date


def main():
    prenom = input("Ton prénom : ")
    age = int(input("Ton âge : "))
    annee_naissance = date.today().year - age
    print(f"Bonjour, {prenom}, tu as {age} ans, donc tu es né(e) vers {annee_naissance}.")


if __name__ == "__main__":
    main()
