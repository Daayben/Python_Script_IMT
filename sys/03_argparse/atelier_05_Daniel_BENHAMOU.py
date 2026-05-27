import argparse


def vers_celsius(valeur: float, unite: str) -> float:
    if unite == "celsius":
        return valeur
    if unite == "fahrenheit":
        return (valeur - 32) * 5 / 9
    return valeur - 273.15  # kelvin


def depuis_celsius(valeur: float, unite: str) -> float:
    if unite == "celsius":
        return valeur
    if unite == "fahrenheit":
        return valeur * 9 / 5 + 32
    return valeur + 273.15  # kelvin


def main():
    parser = argparse.ArgumentParser(description="Convertisseur de température")
    parser.add_argument("valeur", type=float, help="Température à convertir")
    parser.add_argument(
        "--from", dest="depuis",
        choices=["celsius", "fahrenheit", "kelvin"], required=True,
    )
    parser.add_argument(
        "--to", dest="vers",
        choices=["celsius", "fahrenheit", "kelvin"], required=True,
    )
    parser.add_argument("--precision", type=int, default=2)
    args = parser.parse_args()

    resultat = depuis_celsius(vers_celsius(args.valeur, args.depuis), args.vers)
    fmt = f".{args.precision}f"
    print(f"{args.valeur:{fmt}} {args.depuis} = {resultat:{fmt}} {args.vers}")


if __name__ == "__main__":
    main()
