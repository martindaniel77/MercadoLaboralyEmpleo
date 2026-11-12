"""
Vista 3 — Comportamiento Temporal (2021–2026).

Pregunta: ¿Cómo ha evolucionado el volumen de trabajadores, el ingreso neto y
la intensidad horaria semanal a lo largo de los seis años analizados?
"""

from services.common import (
    COLOR_TIPO_PLATAFORMA,
    TIPOS_PLATAFORMA,
    _cop,
    _run,
)


def _line_chart(labels, series, ref=None, ymin=None, ymax=None):
    """Construye los datos de un gráfico de líneas SVG (series temporales)."""
    width, height = 560, 260
    left, right, top, bottom = 44, 14, 16, 34
    plot_w = width - left - right
    plot_h = height - top - bottom

    all_vals = [v for s in series for v in s['values']]
    if ymin is None:
        ymin = min(all_vals) - 2
    if ymax is None:
        ymax = max(all_vals) + 2
    n = len(labels)

    def _x(i):
        return left + (plot_w * i / (n - 1)) if n > 1 else left + plot_w / 2.0

    def _y(v):
        return top + plot_h * (1 - (v - ymin) / (ymax - ymin))

    out_series = []
    for s in series:
        pts = [f'{_x(i):.1f},{_y(v):.1f}' for i, v in enumerate(s['values'])]
        dots = [{'cx': f'{_x(i):.1f}', 'cy': f'{_y(v):.1f}', 'v': v}
                for i, v in enumerate(s['values'])]
        out_series.append({'name': s['name'], 'color': s['color'],
                           'points': ' '.join(pts), 'dots': dots})

    ref_line = None
    if ref is not None:
        ref_line = {'y': round(_y(ref), 1), 'label': f'{ref:g}'}

    return {
        'labels': labels,
        'series': out_series,
        'ref': ref_line,
        'ymin': ymin,
        'ymax': ymax,
        'width': width,
        'height': height,
        'left': left,
        'right': right,
        'top': top,
        'bottom': bottom,
        'ticks': [{'x': f'{_x(i):.1f}', 'label': str(labels[i])} for i in range(n)],
        'y_min_label': f'{ymin:g}',
        'y_max_label': f'{ymax:g}',
    }


def get_vista3(filtros=None):
    """Retorna todos los datos de la Vista 3 (Comportamiento Temporal 2021–2026).

    Filtros soportados (operaciones Slice/Dice):
      - tipo : valor de dim_plataforma.tipo_plataforma o 'Todos'
      - pais : valor de dim_geografia.pais o 'Todos'
      - nivel: 'anio' (Roll-up) o 'trimestre' (Drill-down) de la jerarquía
               dim_tiempo.anio -> trimestre -> mes
      - pivot: 'anio_tipo' o 'tipo_anio' (operación Pivot de la matriz)
    """
    filtros = dict(filtros or {})
    filtros.setdefault('tipo', 'Todos')
    filtros.setdefault('pais', 'Todos')
    filtros.setdefault('nivel', 'anio')
    filtros.setdefault('pivot', 'anio_tipo')

    conds = []
    params = {}
    if filtros.get('tipo') and filtros['tipo'] != 'Todos':
        conds.append('p.tipo_plataforma = :tipo')
        params['tipo'] = filtros['tipo']
    if filtros.get('pais') and filtros['pais'] != 'Todos':
        conds.append('g.pais = :pais')
        params['pais'] = filtros['pais']
    where = (' WHERE ' + ' AND '.join(conds)) if conds else ''

    _FROM = (
        'FROM fact_gig_economy f '
        'JOIN dim_tiempo ti ON ti.id_tiempo = f.id_tiempo '
        'JOIN dim_plataforma p ON p.id_plataforma = f.id_plataforma '
        'JOIN dim_geografia g ON g.id_geografia = f.id_geografia'
    )

    # ---- Universo e indicadores (KPIs) ----
    total = _run(f'SELECT COUNT(DISTINCT f.id_trabajador) {_FROM}{where}', params)[0][0]
    jornada = _run(f'SELECT AVG(f.horas_semanales) {_FROM}{where}', params)[0][0]

    ing_2021 = _run(
        f'SELECT AVG(f.ingreso_neto_mensual_cop) {_FROM}{where} AND ti.anio = 2021', params)[0][0]
    ing_2025 = _run(
        f'SELECT AVG(f.ingreso_neto_mensual_cop) {_FROM}{where} AND ti.anio = 2025', params)[0][0]
    variacion = 0.0
    if ing_2021 and float(ing_2021) > 0:
        variacion = (float(ing_2025) - float(ing_2021)) / float(ing_2021) * 100

    kpis = [
        {
            'valor': f'{total:,}'.replace(',', '.'),
            'unidad': 'trabajadores',
            'label': 'Volumen de trabajadores (2021–2026)',
            'sub': '2026 es corte parcial (enero–junio), no comparable directo',
        },
        {
            'valor': f'{float(jornada):.1f}'.replace('.', ',') + ' h',
            'unidad': 'horas / semana',
            'label': 'Intensidad horaria promedio',
            'sub': 'Límite legal colombiano: 47 h/semana',
        },
        {
            'valor': f'{variacion:+.1f}'.replace('.', ',') + '%',
            'unidad': '2021 → 2025',
            'label': 'Variación del ingreso neto (periodos equivalentes)',
            'sub': f'${_cop(ing_2021)} → ${_cop(ing_2025)} COP',
        },
    ]

    # ---- Viz 1: volumen por nivel temporal (Drill-down / Roll-up) ----
    if filtros['nivel'] == 'trimestre':
        vol_rows = _run(
            f'SELECT ti.anio, ti.trimestre, COUNT(DISTINCT f.id_trabajador) {_FROM}{where} '
            'GROUP BY ti.anio, ti.trimestre ORDER BY ti.anio, ti.trimestre',
            params,
        )
        columns = [
            {'label': f'{anio % 100}T{tri[-1]}', 'value': v,
             'partial': anio == 2026}
            for anio, tri, v in vol_rows
        ]
        vol_titulo = 'Volumen de trabajadores por trimestre'
        vol_subtitulo = 'Drill-down: de año a trimestre (2026 en color de corte parcial)'
    else:
        vol_rows = _run(
            f'SELECT ti.anio, COUNT(DISTINCT f.id_trabajador) {_FROM}{where} '
            'GROUP BY ti.anio ORDER BY ti.anio',
            params,
        )
        columns = [
            {'label': str(anio), 'value': v, 'partial': anio == 2026}
            for anio, v in vol_rows
        ]
        vol_titulo = 'Volumen de trabajadores por año'
        vol_subtitulo = 'Roll-up: nivel superior de la jerarquía temporal'

    viz1 = {
        'titulo': vol_titulo,
        'subtitulo': vol_subtitulo,
        'nivel': filtros['nivel'],
        'columns': columns,
        'max': max((c['value'] for c in columns), default=1),
    }

    # ---- Viz 2: jornada semanal por año x tipo (gráfico de líneas) ----
    anios = sorted({r[0] for r in _run(f'SELECT ti.anio {_FROM}{where} GROUP BY ti.anio', params)})
    jornada_series = {}
    for tipo in TIPOS_PLATAFORMA:
        rows = _run(
            f'SELECT ti.anio, AVG(f.horas_semanales) {_FROM}{where} '
            f"AND p.tipo_plataforma = '{tipo}' GROUP BY ti.anio ORDER BY ti.anio",
            params,
        )
        jornada_series[tipo] = {a: float(v) for a, v in rows}

    line_series = []
    for tipo in TIPOS_PLATAFORMA:
        data_tipo = jornada_series.get(tipo)
        if not data_tipo:
            continue
        line_series.append({
            'name': tipo,
            'color': COLOR_TIPO_PLATAFORMA[tipo],
            'values': [data_tipo.get(a) for a in anios],
        })
    viz2 = _line_chart(anios, line_series, ref=47.0, ymin=30, ymax=56)
    viz2['titulo'] = 'Evolución de la jornada semanal promedio por modelo'
    viz2['subtitulo'] = 'Línea punteada = límite legal (47 h/semana)'
    viz2['series'] = [
        {'name': s['name'], 'color': s['color'], 'points': s['points'],
         'dots': list(s['dots'])}
        for s in viz2['series']
    ]

    # ---- Matriz: anio x tipo de plataforma (ingreso neto promedio) ----
    m_rows = _run(
        f'SELECT ti.anio, p.tipo_plataforma, AVG(f.ingreso_neto_mensual_cop) {_FROM}{where} '
        'GROUP BY ti.anio, p.tipo_plataforma ORDER BY ti.anio, p.tipo_plataforma',
        params,
    )
    m = {}
    for anio, tipo, v in m_rows:
        m[(anio, tipo)] = float(v)
    anios_matriz = sorted({r[0] for r in m_rows})

    if filtros['pivot'] == 'anio_tipo':
        filas = anios_matriz
        columnas = TIPOS_PLATAFORMA
        cells = [[('$' + _cop(m.get((f, c))) if m.get((f, c)) is not None else '—') for c in columnas] for f in filas]
    else:
        filas = TIPOS_PLATAFORMA
        columnas = anios_matriz
        cells = [[('$' + _cop(m.get((c, f))) if m.get((c, f)) is not None else '—') for c in columnas] for f in filas]

    matriz = {
        'filas': filas,
        'columnas': columnas,
        'cells': cells,
        'pivot': filtros['pivot'],
        'medida': 'ingreso_neto_mensual_cop (promedio)',
    }

    paises = [r[0] for r in _run('SELECT DISTINCT g.pais FROM dim_geografia g ORDER BY g.pais')]

    return {
        'titulo': 'Comportamiento Temporal (2021–2026)',
        'pregunta': '¿Cómo ha evolucionado el volumen de trabajadores, el ingreso neto y la intensidad '
                    'horaria semanal a lo largo de los seis años analizados (2021–2026)?',
        'dimensiones': [
            {'nombre': 'dim_tiempo', 'atributos': 'anio, trimestre, mes'},
            {'nombre': 'dim_plataforma', 'atributos': 'tipo_plataforma'},
            {'nombre': 'dim_geografia', 'atributos': 'pais'},
        ],
        'medidas': [
            {'nombre': 'Volumen de trabajadores', 'formula': 'COUNT(DISTINCT id_trabajador)',
             'agregacion': 'Conteo de entidades únicas por periodo'},
            {'nombre': 'Ingreso neto mensual', 'formula': 'AVG(ingreso_neto_mensual_cop)',
             'agregacion': 'Promedio aritmético (recalculado por periodo)'},
            {'nombre': 'Intensidad horaria', 'formula': 'AVG(horas_semanales)',
             'agregacion': 'Promedio aritmético'},
        ],
        'jerarquias': [
            {'nombre': 'Jerarquía temporal',
             'ruta': 'anio → trimestre → mes',
             'operaciones': 'Drill-down / Roll-up'},
        ],
        'filtros': {
            'tipo': {'opciones': TIPOS_PLATAFORMA, 'seleccion': filtros['tipo']},
            'pais': {'opciones': paises, 'seleccion': filtros['pais']},
        },
        'nivel': filtros['nivel'],
        'pivot': filtros['pivot'],
        'total': total,
        'kpis': kpis,
        'viz1': viz1,
        'viz2': viz2,
        'matriz': matriz,
        'seleccion_activa': {
            'tipo': filtros['tipo'],
            'pais': filtros['pais'],
            'nivel': filtros['nivel'],
            'pivot': filtros['pivot'],
        },
        'conocimientos': _conocimientos_vista3(),
        'interpretacion': (
            'La serie 2021–2026 no muestra un mercado en expansión sino un mercado saturado y estable: '
            'el volumen anual oscila entre 2.198 y 2.292 trabajadores en los años completos (promedio '
            '~2.248), sin pico en 2024. La aparente caída de 2026 (1.109) es un artefacto del corte '
            'parcial del año (enero–junio). La intensidad horaria permanece congelada: 52–53 h/semana en '
            'plataformas físicas (por encima del límite legal de 47 h) y 33–34 h en línea, sin mejora en '
            'seis años. El ingreso neto nominal apenas varía (+3,0% entre 2021 y 2025), con el segmento en '
            'línea estancado e incluso levemente a la baja, lo que contradice la idea de un auge de ingresos.'
        ),
        'limitacion': (
            'El año 2026 es un corte parcial (enero–junio) y no debe compararse como un periodo completo '
            'sin anualizar. Los ingresos se expresan en valores nominales sin deflactar por inflación, por '
            'lo que un crecimiento de +3,0% puede implicar pérdida real de poder adquisitivo. Además, los '
            'registros son transversales, no un panel: no puede saberse si el mismo trabajador permanece '
            'activo entre años.'
        ),
        'decision': (
            'Implementar mecanismos algorítmicos de desconexión y alertas de fatiga en aplicaciones de '
            'reparto y transporte, dado que la jornada física supera el límite legal en los seis años '
            'analizados (52–53 h/semana), y estandarizar el reporte anual anualizando el corte de 2026 '
            'para evitar lecturas erróneas de caída del mercado.'
        ),
    }


def _conocimientos_vista3():
    """Dos conocimientos multidimensionales de la Vista 3 (estructura de 8 campos)."""
    return [
        {
            'id': 'KM-3.1',
            'titulo': 'Mercado saturado, no en auge: volumen estable y corte parcial de 2026',
            'pregunta': '¿El mercado de plataformas siguió creciendo entre 2021 y 2026 o alcanzó una meseta?',
            'dimensiones_medidas': 'dim_tiempo.anio y trimestre; medida = Volumen de trabajadores '
                                   '(COUNT DISTINCT).',
            'procedimiento': 'Roll-up (agrupación por año) y comparación de periodos equivalentes '
                             '(2021–2025 completos vs 2026 parcial). Drill-down a trimestre para verificar '
                             'estabilidad intranual.',
            'evidencia': 'Visualización 1 (columnas por año y por trimestre).',
            'hallazgo': 'El volumen anual 2021–2025 se mantiene entre 2.198 y 2.292 trabajadores (promedio '
                        '2.248); 2024 (2.223) no es un pico, incluso es inferior a 2022 (2.292). El valor de '
                        '2026 (1.109) cubre solo dos trimestres y, anualizado, equivaldría a ~2.218. El '
                        'desglose trimestral confirma estabilidad (~530–600 registros por trimestre) sin '
                        'estacionalidad relevante.',
            'interpretacion': 'Corrige el hallazgo K3.3 de la Etapa 4 (que reportaba un pico en 2024): el '
                             'modelo multidimensional, con granularidad de hechos consistente, muestra una '
                             'meseta de saturación y no un boom. La lectura ingenua de 2026 como "colapso" '
                             'viola la condición de comparar periodos equivalentes.',
            'utilidad': 'Evita sobreestimar la demanda de empleo en plataformas y orienta la planeación de '
                        'capacidad de atención en salud y seguridad vial hacia un colectivo estable, no creciente.',
            'limitacion': 'La granularidad es por fecha de registro (transversal), por lo que no distingue '
                          'nuevas incorporaciones de trabajadores ya activos en años previos.',
        },
        {
            'id': 'KM-3.2',
            'titulo': 'Jornada física crónicamente sobre el límite legal sin traducirse en crecimiento',
            'pregunta': '¿Se redujo la sobrecarga horaria en plataformas físicas entre 2021 y 2026?',
            'dimensiones_medidas': 'dim_tiempo.anio × dim_plataforma.tipo_plataforma; medidas = '
                                   'AVG(horas_semanales) y AVG(ingreso_neto_mensual_cop).',
            'procedimiento': 'Serie temporal anual de jornada e ingreso neto desagregada por modelo de '
                             'plataforma; promedios recalculados por año y modelo.',
            'evidencia': 'Visualización 2 (líneas de jornada con línea de referencia de 47 h) e indicador 3.',
            'hallazgo': 'En los seis años la jornada en plataformas físicas nunca baja de 52,1 h/semana '
                        '(rango 52,1–53,4 h), superando el límite legal de 47 h de forma crónica; en línea se '
                        'mantiene en 33,6–34,6 h. Pese a ello, el ingreso neto físico solo crece +6,4% '
                        '(2.730.231 → 2.905.632 COP, 2021–2025) y el ingreso en línea cae −2,9% en el periodo.',
            'interpretacion': 'Profundiza el hallazgo K3.2: la flexibilidad horaria opera como incentivo '
                             'perverso —la jornada excesiva es permanente y no se traduce en una mejora '
                             'significativa del ingreso nominal, lo que sugiere rendimientos decrecientes y '
                             'una transferencia del riesgo al trabajador.',
            'utilidad': 'Sustenta alertas algorítmicas de fatiga y desconexión obligatoria tras un máximo de '
                        'horas continuas en transporte y reparto.',
            'limitacion': 'Los ingresos son nominales (sin deflactar); las horas incluyen tiempos de espera '
                          'con la aplicación encendida, y no se controla por productividad por hora efectiva.',
        },
    ]
