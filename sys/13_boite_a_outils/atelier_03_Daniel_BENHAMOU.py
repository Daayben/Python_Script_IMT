import secrets
import tempfile
import os


def main():
    token = secrets.token_urlsafe(32)

    with tempfile.TemporaryDirectory() as tmpdir:
        chemin_env = os.path.join(tmpdir, ".env")

        with open(chemin_env, "w", encoding="utf-8") as f:
            f.write(f"TOKEN={token}\n")

        print(f"fichier .env : {chemin_env}")

        with open(chemin_env, encoding="utf-8") as f:
            contenu = f.read().strip()

        print(f"contenu     : {contenu}")

        _, _, valeur = contenu.partition("=")

        identique = secrets.compare_digest(token, valeur)
        print(f"lu          : {valeur}")
        print(f"identique   : {identique}")


if __name__ == "__main__":
    main()
