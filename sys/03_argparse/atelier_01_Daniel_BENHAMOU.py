import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Mini-calculatrice en ligne de commande")
    parser.add_argument("a", type=float, help="Premier nombre")
    parser.add_argument("op", choices=["+", "-", "*", "/"], help="Opérateur")
    parser.add_argument("b", type=float, help="Deuxième nombre")
    args = parser.parse_args()

    if args.op == "/" and args.b == 0:
        print("Erreur : division par zéro", file=sys.stderr)
        sys.exit(1)

    resultats = {
        "+": args.a + args.b,
        "-": args.a - args.b,
        "*": args.a * args.b,
        "/": args.a / args.b,
    }
    print(f"{args.a} {args.op} {args.b} = {resultats[args.op]}")


if __name__ == "__main__":
    main()
