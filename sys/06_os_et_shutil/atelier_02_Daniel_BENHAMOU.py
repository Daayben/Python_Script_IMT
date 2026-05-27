import argparse
import shutil
from datetime import datetime
from pathlib import Path


def backup(source: Path) -> Path:
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = source.parent / f"backup_{horodatage}"
    shutil.copytree(source, destination)
    nb_fichiers = sum(1 for _ in destination.rglob("*") if _.is_file())
    print(f"Backup créé : {destination}")
    print(f"Fichiers copiés : {nb_fichiers}")
    return destination


def main():
    parser = argparse.ArgumentParser(
        description="Copier un dossier vers backup_YYYYMMDD_HHMMSS/"
    )
    parser.add_argument("source", help="Chemin du dossier source")
    args = parser.parse_args()
    backup(Path(args.source))


if __name__ == "__main__":
    main()
