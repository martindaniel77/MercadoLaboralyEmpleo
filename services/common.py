"""
Utilidades compartidas del análisis multidimensional (Etapa 5).

Contiene las constantes (paletas de color, órdenes canónicos, dominios) y los
helpers de consulta/formato que reutilizan los servicios de cada vista. Todos
los servicios consultan el modelo estrella implementado en PostgreSQL
(fact_gig_economy + dim_tiempo / dim_geografia / dim_plataforma / dim_trabajador).
"""

from sqlalchemy import text

from database import db


# ---------------------------------------------------------------------------
# Paletas y órdenes canónicos
# ---------------------------------------------------------------------------

COLOR_TIPO_PLATAFORMA = {
    'Fisica / Basada en Ubicacion': '#edbd4c',
    'En linea / Basada en la Nube': '#3e7cb1',
}

COLOR_GENERO = {
    'Masculino': '#2b2314',
    'Femenino': '#edbd4c',
    'No binario / Otro': '#b8a886',
}

ORDEN_EDUCATIVO = [
    'Primaria',
    'Secundaria / Bachillerato',
    'Tecnico / Tecnologo',
    'Universitario',
    'Posgrado',
]

GENEROS = ['Masculino', 'Femenino', 'No binario / Otro']
TIPOS_PLATAFORMA = ['Fisica / Basada en Ubicacion', 'En linea / Basada en la Nube']


# ---------------------------------------------------------------------------
# Utilidades de consulta y formato
# ---------------------------------------------------------------------------

def _run(sql, params=None):
    """Ejecuta una consulta contra el modelo y devuelve la lista de filas."""
    result = db.session.execute(text(sql), params or {})
    return [tuple(row) for row in result.fetchall()]


def _pct(numerador, denominador):
    if not denominador:
        return 0.0
    return round((numerador / denominador) * 100, 1)


def _ordenar_educativo(par_dict):
    """Ordena un dict {nivel_educativo: valor} según el orden ordinal canónico."""
    return {k: par_dict.get(k, 0) for k in ORDEN_EDUCATIVO}


def _usd(v):
    """Formatea un valor USD con coma decimal española."""
    return f'{v:.2f}'.replace('.', ',')


def _cop(v):
    """Formatea un valor COP con separador de miles español."""
    return f'{int(round(v)):,}'.replace(',', '.')
