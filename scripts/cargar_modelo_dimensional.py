import os

import pandas as pd
from sqlalchemy import create_engine, text

from database import URI_DB, db
import models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "dataMultidimensional")

ORDEN_CARGA = [
    ("dim_tiempo", "dim_tiempo.csv", "fecha_registro"),
    ("dim_geografia", "dim_geografia.csv", None),
    ("dim_plataforma", "dim_plataforma.csv", None),
    ("dim_trabajador", "dim_trabajador.csv", None),
    ("fact_gig_economy", "fact_gig_economy.csv", None),
]

SECUENCIAS = [
    ("dim_tiempo", "id_tiempo"),
    ("dim_geografia", "id_geografia"),
    ("dim_plataforma", "id_plataforma"),
    ("dim_trabajador", "id_trabajador"),
    ("fact_gig_economy", "id_hecho"),
]

TABLAS = [t for t, _, _ in ORDEN_CARGA]


def cargar_dataframe(engine, tabla, archivo, col_fecha):
    ruta = os.path.join(DATA_DIR, archivo)
    df = pd.read_csv(ruta)
    if col_fecha:
        df[col_fecha] = pd.to_datetime(df[col_fecha]).dt.date
    df.to_sql(tabla, engine, if_exists="append", index=False)
    return len(df)


def resetear_secuencias(engine):
    with engine.begin() as conn:
        for tabla, id_col in SECUENCIAS:
            conn.execute(
                text(
                    f"SELECT setval(pg_get_serial_sequence('{tabla}', '{id_col}'), "
                    f"COALESCE((SELECT MAX({id_col}) FROM {tabla}), 1))"
                )
            )


def main():
    engine = create_engine(URI_DB)

    db.metadata.create_all(engine)

    with engine.begin() as conn:
        conn.execute(
            text(f"TRUNCATE TABLE {', '.join(TABLAS)} CASCADE")
        )

    totales = {}
    for tabla, archivo, col_fecha in ORDEN_CARGA:
        n = cargar_dataframe(engine, tabla, archivo, col_fecha)
        totales[tabla] = n
        print(f"{tabla}: {n} filas insertadas")

    resetear_secuencias(engine)
    print("Secuencias actualizadas correctamente.")

    print("\nResumen de carga:")
    for tabla in TABLAS:
        print(f"  - {tabla}: {totales[tabla]} filas")


if __name__ == "__main__":
    main()
