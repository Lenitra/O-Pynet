import os
from collections import defaultdict

# Liste des extensions de fichiers à prendre en compte
VALID_EXTENSIONS = {".py", ".txt", ".md", ".html", ".js", ".css"}  # Vous pouvez ajouter d'autres extensions ici


def count_lines_by_extension(root_dir, valid_extensions):
    line_counts = defaultdict(int)

    # Parcours récursif de l'arborescence
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            file_extension = os.path.splitext(file)[1]
            if file_extension in valid_extensions:
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        line_count = sum(1 for _ in f)
                        line_counts[file_extension] += line_count
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}")

    return line_counts


def main():
    root_dir = os.path.dirname(
        os.path.abspath(__file__)
    )  # Current directory of the script
    line_counts = count_lines_by_extension(root_dir, VALID_EXTENSIONS)

    # Afficher les résultats triés par extension
    for extension, count in sorted(line_counts.items()):
        print(f"{extension}: {count} lines")


if __name__ == "__main__":
    main()
