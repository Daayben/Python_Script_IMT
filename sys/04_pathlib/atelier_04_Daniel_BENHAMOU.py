from pathlib import Path


def decomposer(chemin: str) -> tuple[str, str, str]:
    p = Path(chemin)
    return str(p.parent), p.stem, p.suffix


if __name__ == "__main__":
    exemples = [
        "/tmp/a.txt",
        "/var/log/archive.tar.gz",
        "/etc/hosts",
    ]
    for c in exemples:
        print(f"{c:<30} -> {decomposer(c)}")
