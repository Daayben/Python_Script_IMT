import tarfile
import tempfile
from pathlib import Path


def creer_archive(dossier: Path) -> Path:
    archive = dossier / "archive.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        for fichier in dossier.glob("*.txt"):
            tar.add(fichier, arcname=fichier.name)
    return archive


def extraire_archive(archive: Path, cible: Path) -> list[Path]:
    cible.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(cible, filter="data")
    return sorted(p for p in cible.rglob("*") if p.is_file())


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        dossier = Path(tmp)

        for nom, contenu in [("a.txt", "alpha"), ("b.txt", "beta"), ("c.txt", "gamma")]:
            (dossier / nom).write_text(contenu, encoding="utf-8")

        archive = creer_archive(dossier)
        print(f"Archive créée : {archive.name}")

        cible = dossier / "cible"
        fichiers = extraire_archive(archive, cible)
        print("Fichiers extraits :")
        for f in fichiers:
            print(f"  {f.name} : {f.read_text(encoding='utf-8')!r}")
