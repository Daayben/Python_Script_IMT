import argparse
import datetime

LOG = "app.log"


def journaliser(message: str) -> None:
    horodatage = datetime.datetime.now().isoformat(timespec="seconds")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{horodatage} {message}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ajouter une entrée horodatée dans app.log"
    )
    parser.add_argument("message", help="Message à journaliser")
    args = parser.parse_args()
    journaliser(args.message)
