import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SRC = os.path.join(PROJECT_ROOT, "data", "dataset_gig_economy_tratado.csv")
OUT = os.path.join(BASE_DIR, "dim_tiempo.csv")


def trimestre(mes):
    return "T" + str((mes - 1) // 3 + 1)


def main():
    fechas = set()
    with open(SRC, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            fechas.add(row["fecha_registro"])

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id_tiempo", "anio", "mes", "trimestre", "fecha_registro"])
        for i, fecha in enumerate(sorted(fechas), start=1):
            anio = int(fecha[0:4])
            mes = int(fecha[5:7])
            w.writerow([i, anio, mes, trimestre(mes), fecha])

    print(f"dim_tiempo.csv generado con {len(fechas)} filas")


if __name__ == "__main__":
    main()
