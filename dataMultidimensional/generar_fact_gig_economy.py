import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
SRC = os.path.join(PROJECT_ROOT, "data", "dataset_gig_economy_tratado.csv")
OUT = os.path.join(BASE_DIR, "fact_gig_economy.csv")

GEO_COLS = [
    "nivel_territorial",
    "pais",
    "codigo_iso_pais",
    "departamento_region",
    "ciudad_municipio",
]
PLAT_COLS = ["tipo_plataforma", "categoria_servicio", "plataforma_principal"]
MEASURES = [
    "ingreso_bruto_mensual_cop",
    "costos_operativos_mensuales_cop",
    "ingreso_neto_mensual_cop",
    "ingreso_neto_hora_usd",
    "horas_semanales",
    "calificacion_promedio_app",
]


def cargar_mapeo(filename, key_cols, id_col):
    mapeo = {}
    path = os.path.join(BASE_DIR, filename)
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            clave = tuple(row[c] for c in key_cols)
            mapeo[clave] = row[id_col]
    return mapeo


def main():
    tiempo = cargar_mapeo("dim_tiempo.csv", ["fecha_registro"], "id_tiempo")
    geografia = cargar_mapeo("dim_geografia.csv", GEO_COLS, "id_geografia")
    plataforma = cargar_mapeo("dim_plataforma.csv", PLAT_COLS, "id_plataforma")
    trabajador = cargar_mapeo("dim_trabajador.csv", ["id_registro"], "id_trabajador")

    n = 0
    with open(SRC, encoding="utf-8-sig", newline="") as fin, open(
        OUT, "w", encoding="utf-8", newline=""
    ) as fout:
        w = csv.writer(fout)
        w.writerow(
            ["id_hecho", "id_tiempo", "id_geografia", "id_plataforma", "id_trabajador"]
            + MEASURES
        )
        for i, row in enumerate(csv.DictReader(fin), start=1):
            id_tiempo = tiempo[(row["fecha_registro"],)]
            id_geografia = geografia[tuple(row[c] for c in GEO_COLS)]
            id_plataforma = plataforma[tuple(row[c] for c in PLAT_COLS)]
            id_trabajador = trabajador[(row["id_registro"],)]
            w.writerow(
                [i, id_tiempo, id_geografia, id_plataforma, id_trabajador]
                + [row[m] for m in MEASURES]
            )
            n += 1

    print(f"fact_gig_economy.csv generado con {n} filas")


if __name__ == "__main__":
    main()
