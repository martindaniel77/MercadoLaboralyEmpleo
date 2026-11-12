import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SRC = os.path.join(PROJECT_ROOT, "data", "dataset_gig_economy_tratado.csv")
OUT = os.path.join(BASE_DIR, "dim_trabajador.csv")

COLS = [
    "id_registro",
    "edad",
    "genero",
    "nivel_educativo",
    "antiguedad_meses",
    "dependencia_ingresos",
    "afiliacion_salud",
    "afiliacion_pension",
    "cuenta_con_arl",
    "fuente_origen_id",
]


def main():
    trabajadores = {}
    with open(SRC, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            trabajadores[row["id_registro"]] = {c: row[c] for c in COLS}

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id_trabajador"] + COLS)
        for i, reg in enumerate(sorted(trabajadores), start=1):
            t = trabajadores[reg]
            w.writerow([i] + [t[c] for c in COLS])

    print(f"dim_trabajador.csv generado con {len(trabajadores)} filas")


if __name__ == "__main__":
    main()
