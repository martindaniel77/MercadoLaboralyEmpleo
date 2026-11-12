"""
Vista 1 — Composición y Distribución de la población.

Pregunta: ¿Cómo está compuesta la población de trabajadores de plataformas
digitales según tipo de plataforma, categoría de servicio, género y nivel
educativo, y cómo cambia esa composición al variar la escala territorial?
"""

import math

from services.common import (
    COLOR_GENERO,
    COLOR_TIPO_PLATAFORMA,
    GENEROS,
    ORDEN_EDUCATIVO,
    TIPOS_PLATAFORMA,
    _pct,
    _run,
)


def _build_filters(filtros):
    """Construye la cláusula WHERE dinámica a partir de los filtros activos.

    Los filtros corresponden a atributos de dimensiones distintas (Slice/Dice):
      - pais   -> dim_geografia.pais
      - genero -> dim_trabajador.genero
    """
    conds = []
    params = {}
    if filtros.get('pais') and filtros['pais'] != 'Todos':
        conds.append('g.pais = :pais')
        params['pais'] = filtros['pais']
    if filtros.get('genero') and filtros['genero'] != 'Todos':
        conds.append('t.genero = :genero')
        params['genero'] = filtros['genero']
    where = (' WHERE ' + ' AND '.join(conds)) if conds else ''
    return where, params


_BASE_FROM = (
    'FROM fact_gig_economy f '
    'JOIN dim_plataforma p ON p.id_plataforma = f.id_plataforma '
    'JOIN dim_trabajador t ON t.id_trabajador = f.id_trabajador '
    'JOIN dim_geografia g ON g.id_geografia = f.id_geografia'
)


def _donut_segments(items, radius=42.0, stroke=18.0):
    """Convierte una lista de {label, value, color} en segmentos SVG (donut)."""
    total = sum(i['value'] for i in items) or 1
    circ = 2 * math.pi * radius
    segments = []
    offset = 0.0
    for it in items:
        frac = it['value'] / total
        seg_len = frac * circ
        segments.append({
            'label': it['label'],
            'value': it['value'],
            'pct': round(frac * 100, 1),
            'color': it['color'],
            'dasharray': f'{seg_len:.3f} {circ - seg_len:.3f}',
            'dashoffset': round(-offset, 3),
        })
        offset += seg_len
    return segments, total


def get_vista1(filtros=None):
    """Retorna todos los datos de la Vista 1 (Composición y Distribución).

    Filtros soportados (operaciones Slice/Dice):
      - pais   : valor de dim_geografia.pais o 'Todos'
      - genero : valor de dim_trabajador.genero o 'Todos'
      - nivel  : 'tipo' (Roll-up) o 'categoria' (Drill-down) de la jerarquía
                 dim_plataforma.tipo_plataforma -> categoria_servicio
      - pivot  : 'educacion_tipo' o 'tipo_educacion' (operación Pivot de la matriz)
    """
    filtros = dict(filtros or {})
    filtros.setdefault('pais', 'Todos')
    filtros.setdefault('genero', 'Todos')
    filtros.setdefault('nivel', 'tipo')
    filtros.setdefault('pivot', 'educacion_tipo')

    where, params = _build_filters(filtros)

    # ---- Universo y opciones de los filtros ----
    total = _run(f'SELECT COUNT(DISTINCT f.id_trabajador) {_BASE_FROM}{where}', params)[0][0]

    paises = [r[0] for r in _run(
        'SELECT DISTINCT g.pais FROM dim_geografia g ORDER BY g.pais')]

    # ---- Composición por tipo / categoría de plataforma (Viz 1) ----
    if filtros['nivel'] == 'categoria':
        comp = _run(
            'SELECT p.categoria_servicio, p.tipo_plataforma, '
            f'COUNT(DISTINCT f.id_trabajador) {_BASE_FROM}{where} '
            'GROUP BY p.categoria_servicio, p.tipo_plataforma '
            'ORDER BY COUNT(DISTINCT f.id_trabajador) DESC',
            params,
        )
        comp_tipo = _run(
            'SELECT p.tipo_plataforma, COUNT(DISTINCT f.id_trabajador) '
            f'{_BASE_FROM}{where} GROUP BY p.tipo_plataforma', params)
    else:
        comp = _run(
            'SELECT p.tipo_plataforma, COUNT(DISTINCT f.id_trabajador) '
            f'{_BASE_FROM}{where} GROUP BY p.tipo_plataforma '
            'ORDER BY COUNT(DISTINCT f.id_trabajador) DESC',
            params,
        )
        comp_tipo = comp

    # ---- Nivel educativo x género (Viz 2, barras 100% apiladas) ----
    edu_genero_rows = _run(
        'SELECT t.nivel_educativo, t.genero, COUNT(DISTINCT f.id_trabajador) '
        f'{_BASE_FROM}{where} GROUP BY t.nivel_educativo, t.genero',
        params,
    )

    # ---- Matriz nivel educativo x tipo de plataforma (Pivot) ----
    matriz_rows = _run(
        'SELECT t.nivel_educativo, p.tipo_plataforma, COUNT(DISTINCT f.id_trabajador) '
        f'{_BASE_FROM}{where} GROUP BY t.nivel_educativo, p.tipo_plataforma',
        params,
    )

    # ---- Indicadores (KPIs) ----
    tipo_counts = {r[0]: r[1] for r in comp_tipo}
    fisica = tipo_counts.get('Fisica / Basada en Ubicacion', 0)
    en_linea = tipo_counts.get('En linea / Basada en la Nube', 0)

    fem_online = _run(
        'SELECT COUNT(DISTINCT f.id_trabajador) '
        f'{_BASE_FROM}{where} AND t.genero = \'Femenino\' '
        "AND p.tipo_plataforma = 'En linea / Basada en la Nube'",
        params,
    )[0][0]
    fem_fisica = _run(
        'SELECT COUNT(DISTINCT f.id_trabajador) '
        f'{_BASE_FROM}{where} AND t.genero = \'Femenino\' '
        "AND p.tipo_plataforma = 'Fisica / Basada en Ubicacion'",
        params,
    )[0][0]

    # ---- Preparación de estructuras para el template ----
    # Viz 1: donut (tipo) o barras horizontales (categoría)
    if filtros['nivel'] == 'categoria':
        viz1 = {
            'tipo': 'barras',
            'titulo': 'Distribución por Categoría de Servicio',
            'subtitulo': 'Drill-down: de tipo de plataforma a categoría de servicio '
                        '(color = tipo de plataforma)',
            'barras': [
                {
                    'label': c,
                    'tipo': t,
                    'value': v,
                    'pct': _pct(v, total),
                    'color': COLOR_TIPO_PLATAFORMA.get(t, '#b8a886'),
                }
                for c, t, v in comp
            ],
            'max': max([v for _, _, v in comp], default=1),
        }
    else:
        items = [
            {'label': 'Fisica / Basada en Ubicacion', 'value': fisica,
             'color': COLOR_TIPO_PLATAFORMA['Fisica / Basada en Ubicacion']},
            {'label': 'En linea / Basada en la Nube', 'value': en_linea,
             'color': COLOR_TIPO_PLATAFORMA['En linea / Basada en la Nube']},
        ]
        segments, _ = _donut_segments(items)
        viz1 = {
            'tipo': 'donut',
            'titulo': 'Distribución por Tipo de Plataforma',
            'subtitulo': 'Roll-up: nivel superior de la jerarquía de plataforma',
            'segments': segments,
            'total': total,
        }

    # Viz 2: nivel educativo x género (100% apiladas)
    edu_genero = {}
    for edu, gen, v in edu_genero_rows:
        edu_genero.setdefault(edu, {})[gen] = v
    viz2_categories = [e for e in ORDEN_EDUCATIVO if e in edu_genero]
    viz2_series = []
    for gen in GENEROS:
        values = []
        for edu in viz2_categories:
            v = edu_genero.get(edu, {}).get(gen, 0)
            row_total = sum(edu_genero.get(edu, {}).values()) or 1
            values.append({'value': v, 'pct': _pct(v, row_total)})
        viz2_series.append({
            'name': gen,
            'color': COLOR_GENERO.get(gen, '#b8a886'),
            'values': values,
        })
    viz2 = {
        'titulo': 'Composición por Género dentro de cada Nivel Educativo',
        'subtitulo': 'Barras 100% apiladas (denominador = total del nivel educativo)',
        'categories': viz2_categories,
        'series': viz2_series,
    }

    # Matriz: pivot entre educación x tipo y tipo x educación
    m = {}
    for edu, tipo, v in matriz_rows:
        m[(edu, tipo)] = v
    if filtros['pivot'] == 'educacion_tipo':
        filas = [e for e in ORDEN_EDUCATIVO if any((e, t) in m for t in TIPOS_PLATAFORMA)]
        columnas = TIPOS_PLATAFORMA
        cells = [[m.get((f, c), 0) for c in columnas] for f in filas]
    else:
        filas = TIPOS_PLATAFORMA
        columnas = [e for e in ORDEN_EDUCATIVO if any((e, t) in m for t in TIPOS_PLATAFORMA)]
        cells = [[m.get((c, f), 0) for c in columnas] for f in filas]

    row_totals = [sum(row) for row in cells]
    col_totals = [sum(cells[r][c] for r in range(len(filas))) for c in range(len(columnas))]
    grand = sum(row_totals)

    matriz = {
        'filas': filas,
        'columnas': columnas,
        'cells': cells,
        'row_totals': row_totals,
        'col_totals': col_totals,
        'grand': grand,
        'pivot': filtros['pivot'],
    }

    # ---- KPIs ----
    kpis = [
        {
            'valor': f'{total:,}'.replace(',', '.'),
            'unidad': 'trabajadores',
            'label': 'Total de trabajadores (entidades únicas)',
            'sub': 'Conteo DISTINCT de id_trabajador en la tabla de hechos',
        },
        {
            'valor': f'{_pct(fisica, total)}%'.replace('.', ','),
            'unidad': f'{fisica:,}'.replace(',', '.') + ' trabajadores',
            'label': 'Participación de plataformas físicas',
            'sub': 'Transporte, reparto y servicios del hogar',
        },
        {
            'valor': f'{_pct(fem_online, en_linea)}%'.replace('.', ','),
            'unidad': 'participación femenina en línea',
            'label': 'Índice de feminización del trabajo en línea',
            'sub': f'vs {_pct(fem_fisica, fisica)}%'.replace('.', ',') + ' en plataformas físicas',
        },
    ]

    return {
        'titulo': 'Composición y Distribución de la Población',
        'pregunta': '¿Cómo está compuesta la población de trabajadores de plataformas digitales '
                    'según tipo de plataforma, categoría de servicio, género y nivel educativo, '
                    'y cómo cambia esa composición al variar la escala territorial?',
        'dimensiones': [
            {'nombre': 'dim_plataforma', 'atributos': 'tipo_plataforma, categoria_servicio'},
            {'nombre': 'dim_trabajador', 'atributos': 'genero, nivel_educativo'},
            {'nombre': 'dim_geografia', 'atributos': 'pais, nivel_territorial, departamento_region'},
        ],
        'medidas': [
            {'nombre': 'Total de trabajadores', 'formula': 'COUNT(DISTINCT id_trabajador)',
             'agregacion': 'Conteo de entidades únicas (no suma de cantidades)'},
        ],
        'jerarquias': [
            {'nombre': 'Jerarquía de plataforma',
             'ruta': 'tipo_plataforma → categoria_servicio → plataforma_principal',
             'operaciones': 'Drill-down / Roll-up'},
            {'nombre': 'Jerarquía geográfica',
             'ruta': 'pais → departamento_region → ciudad_municipio',
             'operaciones': 'Slice (por país)'},
        ],
        'filtros': {
            'pais': {'opciones': paises, 'seleccion': filtros['pais']},
            'genero': {'opciones': GENEROS, 'seleccion': filtros['genero']},
        },
        'nivel': filtros['nivel'],
        'pivot': filtros['pivot'],
        'total': total,
        'kpis': kpis,
        'viz1': viz1,
        'viz2': viz2,
        'matriz': matriz,
        'seleccion_activa': {
            'pais': filtros['pais'],
            'genero': filtros['genero'],
            'nivel': filtros['nivel'],
            'pivot': filtros['pivot'],
        },
        'conocimientos': _conocimientos_vista1(),
        'interpretacion': (
            'La población de la Gig Economy está dominada por el trabajo físico presencial '
            '(65,8% frente a 34,2% en línea) y por una mayoría masculina global (71,4%). Sin embargo, '
            'el cruce multidimensional revela que esa imagen agregada oculta dos segmentaciones '
            'estructurales: por un lado, el capital humano se polariza entre un trabajo físico con '
            'predominio de educación básica y un trabajo digital con alta presencia de educación '
            'universitaria y de posgrado; por otro, la participación femenina casi se duplica al '
            'pasar de las plataformas físicas (20,0%) a las de la nube (38,0%). Estos matices, '
            'invisibles en el análisis descriptivo de la Etapa 4, solo emergen al cruzar las '
            'dimensiones de plataforma, trabajador y territorio.'
        ),
        'limitacion': (
            'El análisis es transversal: cada registro de la tabla de hechos es una fotografía '
            'del trabajador en un periodo y no permite observar la trayectoria de una misma '
            'persona en el tiempo. Además, el grupo "No binario / Otro" representa apenas el 2,4% '
            'de la muestra, por lo que las proporciones de ese segmento no admiten generalizaciones.'
        ),
        'decision': (
            'Focalizar los programas de empleabilidad y cierre de brecha en dos frentes '
            'diferenciados: (1) rutas de certificación tecnológica para los 4.423 trabajadores '
            'con educación secundaria concentrados en el trabajo físico, y (2) protocolos de '
            'seguridad vial y entornos digitales inclusivos para elevar la participación femenina '
            'en transporte, que hoy se sitúa en solo el 20,0%.'
        ),
    }


def _conocimientos_vista1():
    """Dos conocimientos multidimensionales de la Vista 1 (estructura de 8 campos)."""
    return [
        {
            'id': 'KM-1.1',
            'titulo': 'Polarización educativa estructural entre el trabajo físico y el digital',
            'pregunta': '¿Cómo se distribuye el capital humano (nivel educativo) entre las dos '
                        'modalidades de plataforma?',
            'dimensiones_medidas': 'dim_plataforma.tipo_plataforma × dim_trabajador.nivel_educativo; '
                                   'medida = Total de trabajadores (COUNT DISTINCT).',
            'procedimiento': 'Join fact → dim_plataforma y dim_trabajador; agrupación por '
                             'nivel_educativo × tipo_plataforma; proporción por fila con denominador '
                             '= total de cada nivel educativo. Nivel de detalle: 5 × 2 = 10 celdas.',
            'evidencia': 'Matriz nivel educativo × tipo de plataforma y visualización 2.',
            'hallazgo': 'El 95,1% de quienes solo tienen primaria (626 de 658) y el 86,8% de '
                        'secundaria (4.423 de 5.095) operan en plataformas físicas, mientras que el '
                        '83,3% de posgrados (423 de 508) y el 67,6% de universitarios (1.894 de '
                        '2.801) lo hacen en línea. La educación superior (universitario + posgrado) '
                        'constituye el 54,9% de la fuerza en línea, pero solo el 12,2% de la física.',
            'interpretacion': 'Profundiza el conocimiento evidente K1.2: no solo existe un retorno '
                             'nulo al título en el trabajo físico, sino que la formación se '
                             'autoclasifica por modalidad. El trabajo físico absorbe a la población '
                             'menos escolarizada mientras el digital concentra el capital humano, '
                             'reproduciendo una doble vía de inserción laboral desigual.',
            'utilidad': 'Permite orientar programas de reconversión e intermediación laboral '
                        'diferenciados por nivel educativo y modalidad de plataforma.',
            'limitacion': 'Es una asociación transversal observada; no puede concluirse una relación '
                          'causal entre educación y elección de modalidad (pueden mediar factores como '
                          'acceso a conectividad o capital previo).',
        },
        {
            'id': 'KM-1.2',
            'titulo': 'Feminización diferencial: las mujeres se concentran proporcionalmente en línea',
            'pregunta': '¿Difiere la participación femenina entre las plataformas físicas y las '
                        'plataformas en línea?',
            'dimensiones_medidas': 'dim_trabajador.genero × dim_plataforma.tipo_plataforma y '
                                   'categoria_servicio; medida = Total de trabajadores (COUNT DISTINCT).',
            'procedimiento': 'Join fact → dim_trabajador y dim_plataforma; agrupación por '
                             'genero × tipo_plataforma y por genero × categoria_servicio; share '
                             'femenino con denominador = total de cada modalidad. Operaciones: '
                             'Slice (por tipo) y Dice (género × categoría).',
            'evidencia': 'Indicador 3 (índice de feminización) y visualización de género × categoría.',
            'hallazgo': 'En plataformas físicas las mujeres son el 20,0% (1.629 de 8.127), pero en '
                        'línea alcanzan el 38,0% (1.606 de 4.223). Por categoría, la participación '
                        'femenina va del 19,7% en Reparto y Domicilios al 39,0% en Servicios '
                        'Profesionales. El 49,6% de todas las mujeres (1.606 de 3.235) trabaja en '
                        'línea, frente al 28,2% de los hombres (2.485 de 8.823).',
            'interpretacion': 'Matiza el hallazgo K1.3: la mayoría masculina global (71,4%) enmascara '
                             'una composición de género muy distinta por modalidad. La barrera de la '
                             'vía pública (seguridad, jornadas, acceso a vehículo) desplaza a las '
                             'mujeres hacia el trabajo digital, que reduce su brecha de participación.',
            'utilidad': 'Sustenta políticas de cierre de brecha digital femenina y de seguridad vial '
                        'específicas para el transporte de pasajeros y reparto.',
            'limitacion': 'No puede atribuirse causalidad: la sobrerrepresentación femenina en línea '
                          'puede responder a autoselección y no a una barrera verificable en los datos; '
                          'el grupo "No binario / Otro" (292 registros) es insuficiente para generalizar.',
        },
    ]


def get_vista1_opciones_paises():
    """Devuelve la lista de países disponibles para poblar el filtro de territorio."""
    return [r[0] for r in _run('SELECT DISTINCT g.pais FROM dim_geografia g ORDER BY g.pais')]
