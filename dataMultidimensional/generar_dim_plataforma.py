import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SRC = os.path.join(PROJECT_ROOT, "data", "dataset_gig_economy_tratado.csv")
OUT = os.path.join(BASE_DIR, "dim_plataforma.csv")

COLS = ["tipo_plataforma", "categoria_servicio", "plataforma_principal"]


def main():
    combos = set()
    with open(SRC, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            combos.add(tuple(row[c] for c in COLS))

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id_plataforma"] + COLS)
        for i, combo in enumerate(sorted(combos), start=1):
            w.writerow([i] + list(combo))

    print(f"dim_plataforma.csv generado con {len(combos)} filas")


if __name__ == "__main__":
    main()
