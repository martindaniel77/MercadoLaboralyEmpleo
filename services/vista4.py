"""
Vista 4 — Análisis Multivariado: Perfiles, Retorno y Vulnerabilidad.

Pregunta: ¿Qué combinaciones de nivel educativo, modelo de plataforma y horas
dedicadas explican los mayores ingresos netos, y cómo se relaciona esto con la
dependencia económica y la cotización a pensión?
"""

from services.common import (
    COLOR_TIPO_PLATAFORMA,
    ORDEN_EDUCATIVO,
    TIPOS_PLATAFORMA,
    _cop,
    _pct,
    _run,
    _usd,
)


EDU_AGREGADO = [
    ('Basica', ['Primaria', 'Secundaria / Bachillerato']),
    ('Tecnica', ['Tecnico / Tecnologo']),
    ('Superior', ['Universitario', 'Posgrado']),
]

BANDAS_HORAS = [
    '< 30 h', '30-40 h', '40-48 h', '48-56 h', '> 56 h',
]


def _tipo_corto(tipo):
    return 'Física' if 'Fisica' in tipo else 'En línea'


def _banda_horas(h):
    if h < 30:
        return '< 30 h'
    if h < 40:
        return '30-40 h'
    if h < 48:
        return '40-48 h'
    if h < 56:
        return '48-56 h'
    return '> 56 h'


def get_vista4(filtros=None):
    """Retorna todos los datos de la Vista 4 (Análisis Multivariado).

    Filtros soportados (operaciones Slice/Dice):
      - tipo        : valor de dim_plataforma.tipo_plataforma o 'Todos'
      - dependencia : valor de dim_trabajador.dependencia_ingresos o 'Todos'
      - nivel       : 'agregado' (Roll-up) o 'detalle' (Drill-down) de la jerarquía
                      educativa (5 niveles -> 3 grupos)
      - pivot       : 'educacion_tipo' o 'tipo_educacion' (operación Pivot de la matriz)
    """
    filtros = dict(filtros or {})
    filtros.setdefault('tipo', 'Todos')
    filtros.setdefault('dependencia', 'Todos')
    filtros.setdefault('nivel', 'detalle')
    filtros.setdefault('pivot', 'educacion_tipo')

    conds = []
    params = {}
    if filtros.get('tipo') and filtros['tipo'] != 'Todos':
        conds.append('p.tipo_plataforma = :tipo')
        params['tipo'] = filtros['tipo']
    if filtros.get('dependencia') and filtros['dependencia'] != 'Todos':
        conds.append('t.dependencia_ingresos = :dependencia')
        params['dependencia'] = filtros['dependencia']
    where = (' WHERE ' + ' AND '.join(conds)) if conds else ''

    _FROM = (
        'FROM fact_gig_economy f '
        'JOIN dim_trabajador t ON t.id_trabajador = f.id_trabajador '
        'JOIN dim_plataforma p ON p.id_plataforma = f.id_plataforma'
    )

    # ---- Indicadores (KPIs) ----
    total = _run(f'SELECT COUNT(DISTINCT f.id_trabajador) {_FROM}{where}', params)[0][0]
    ingreso_global = _run(
        f'SELECT AVG(f.ingreso_neto_mensual_cop) {_FROM}{where}', params)[0][0]

    edu_avg = {r[0]: float(r[1]) for r in _run(
        f'SELECT t.nivel_educativo, AVG(f.ingreso_neto_mensual_cop) {_FROM}{where} '
        'GROUP BY t.nivel_educativo', params)}
    gradiente = 0.0
    if edu_avg.get('Primaria'):
        gradiente = edu_avg.get('Posgrado', 0) / edu_avg['Primaria']

    cotiza = _run(
        f"SELECT COUNT(DISTINCT f.id_trabajador) {_FROM}{where} AND "
        "t.afiliacion_pension = 'Cotiza activamente'", params)[0][0]

    kpis = [
        {
            'valor': '$' + _cop(ingreso_global),
            'unidad': 'COP / mes',
            'label': 'Ingreso neto mensual promedio',
            'sub': 'Media aritmética de ingreso_neto_mensual_cop',
        },
        {
            'valor': f'{gradiente:.1f}'.replace('.', ',') + 'x',
            'unidad': 'Posgrado vs Primaria',
            'label': 'Gradiente educativo agregado',
            'sub': 'Premio aparente que desaparece al desagregar por modalidad',
        },
        {
            'valor': f'{_pct(cotiza, total)}%'.replace('.', ','),
            'unidad': f'{_cop(cotiza)}' + ' cotizan',
            'label': 'Tasa de cotización a pensión',
            'sub': 'Menor entre dependientes exclusivos de la app',
        },
    ]

    # ---- Viz 1: ingreso neto por nivel educativo x tipo (Drill-down / Roll-up) ----
    edu_rows = _run(
        f'SELECT t.nivel_educativo, p.tipo_plataforma, AVG(f.ingreso_neto_mensual_cop), '
        f'COUNT(DISTINCT f.id_trabajador) {_FROM}{where} '
        'GROUP BY t.nivel_educativo, p.tipo_plataforma',
        params,
    )
    # estructura {(nivel, tipo): (avg, count)}
    raw = {}
    for edu, tipo, v, n in edu_rows:
        raw[(edu, tipo)] = (float(v), n)

    def _grupos_edu():
        if filtros['nivel'] == 'agregado':
            grupos = []
            for gname, miembros in EDU_AGREGADO:
                por_tipo = {}
                for tipo in TIPOS_PLATAFORMA:
                    vals = [raw[(m, tipo)] for m in miembros if (m, tipo) in raw]
                    if vals:
                        tot_n = sum(n for _, n in vals)
                        tot_v = sum(v * n for v, n in vals)
                        por_tipo[tipo] = (tot_v / tot_n, tot_n)
                grupos.append((gname, por_tipo))
            return grupos
        grupos = []
        for edu in ORDEN_EDUCATIVO:
            por_tipo = {}
            for tipo in TIPOS_PLATAFORMA:
                if (edu, tipo) in raw:
                    por_tipo[tipo] = raw[(edu, tipo)]
            if por_tipo:
                grupos.append((edu, por_tipo))
        return grupos

    grupos = _grupos_edu()
    viz1_barras = []
    for gname, por_tipo in grupos:
        for tipo in TIPOS_PLATAFORMA:
            if tipo in por_tipo:
                v, _n = por_tipo[tipo]
                viz1_barras.append({
                    'label': f'{gname} · {_tipo_corto(tipo)}',
                    'value': v,
                    'display': '$' + _cop(v) + ' COP',
                    'color': COLOR_TIPO_PLATAFORMA.get(tipo, '#b8a886'),
                })
    viz1 = {
        'titulo': 'Ingreso neto mensual promedio por nivel educativo y modelo',
        'subtitulo': ('Roll-up: 3 grupos formativos' if filtros['nivel'] == 'agregado'
                      else 'Drill-down: 5 niveles educativos'),
        'nivel': filtros['nivel'],
        'barras': viz1_barras,
        'max': max((b['value'] for b in viz1_barras), default=1.0),
    }

    # ---- Viz 2: tarifa USD/h por banda de jornada ----
    banda_rows = _run(
        f'SELECT f.horas_semanales, p.tipo_plataforma, f.ingreso_neto_hora_usd {_FROM}{where}',
        params,
    )
    banda_agg = {}
    for horas, tipo, usd in banda_rows:
        h = float(horas)
        b = _banda_horas(h)
        banda_agg.setdefault((b, tipo), []).append(float(usd))
    viz2_barras = []
    for b in BANDAS_HORAS:
        for tipo in TIPOS_PLATAFORMA:
            vals = banda_agg.get((b, tipo))
            if vals:
                avg = sum(vals) / len(vals)
                viz2_barras.append({
                    'label': f'{b} · {_tipo_corto(tipo)}',
                    'value': avg,
                    'display': _usd(avg) + ' USD/h',
                    'color': COLOR_TIPO_PLATAFORMA.get(tipo, '#b8a886'),
                })
    viz2 = {
        'titulo': 'Tarifa neta por hora (USD) según banda de jornada semanal',
        'subtitulo': 'La tarifa por hora se devalúa al aumentar las horas (rendimientos decrecientes)',
        'barras': viz2_barras,
        'max': max((b['value'] for b in viz2_barras), default=1.0),
    }

    # ---- Matriz: nivel educativo x tipo de plataforma (ingreso neto promedio) ----
    filas_edu = [gname for gname, _ in grupos]
    m = {}
    for gname, por_tipo in grupos:
        for tipo in TIPOS_PLATAFORMA:
            if tipo in por_tipo:
                m[(gname, tipo)] = por_tipo[tipo][0]

    if filtros['pivot'] == 'educacion_tipo':
        filas = filas_edu
        columnas = TIPOS_PLATAFORMA
        cells = [[('$' + _cop(m.get((f, c))) if m.get((f, c)) is not None else '—') for c in columnas] for f in filas]
    else:
        filas = TIPOS_PLATAFORMA
        columnas = filas_edu
        cells = [[('$' + _cop(m.get((c, f))) if m.get((c, f)) is not None else '—') for c in columnas] for f in filas]

    matriz = {
        'filas': filas,
        'columnas': columnas,
        'cells': cells,
        'pivot': filtros['pivot'],
        'medida': 'ingreso_neto_mensual_cop (promedio)',
    }

    dependencias = [r[0] for r in _run(
        'SELECT DISTINCT t.dependencia_ingresos FROM dim_trabajador t '
        'ORDER BY t.dependencia_ingresos')]

    return {
        'titulo': 'Análisis Multivariado: Perfiles, Retorno y Vulnerabilidad',
        'pregunta': '¿Qué combinaciones de nivel educativo, modelo de plataforma y horas dedicadas explican '
                    'los mayores ingresos netos, y cómo se relaciona esto con la dependencia económica y la '
                    'cotización a pensión?',
        'dimensiones': [
            {'nombre': 'dim_trabajador', 'atributos': 'nivel_educativo, dependencia_ingresos, afiliacion_pension'},
            {'nombre': 'dim_plataforma', 'atributos': 'tipo_plataforma'},
        ],
        'medidas': [
            {'nombre': 'Ingreso neto mensual', 'formula': 'AVG(ingreso_neto_mensual_cop)',
             'agregacion': 'Promedio aritmético (recalculado por celda)'},
            {'nombre': 'Tarifa neta por hora', 'formula': 'AVG(ingreso_neto_hora_usd)',
             'agregacion': 'Promedio aritmético'},
            {'nombre': 'Horas semanales', 'formula': 'horas_semanales (bandas)',
             'agregacion': 'Agrupación por bandas de jornada'},
        ],
        'jerarquias': [
            {'nombre': 'Jerarquía educativa',
             'ruta': 'grupo formativo (Básica / Técnica / Superior) → nivel educativo (5 niveles)',
             'operaciones': 'Drill-down / Roll-up'},
        ],
        'filtros': {
            'tipo': {'opciones': TIPOS_PLATAFORMA, 'seleccion': filtros['tipo']},
            'dependencia': {'opciones': dependencias, 'seleccion': filtros['dependencia']},
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
            'dependencia': filtros['dependencia'],
            'nivel': filtros['nivel'],
            'pivot': filtros['pivot'],
        },
        'conocimientos': _conocimientos_vista4(),
        'interpretacion': (
            'El cruce de nivel educativo, modelo de plataforma y jornada revela que el "premio por educación" '
            'es un efecto de composición: en el agregado existe un gradiente de 2,1x entre Posgrado y Primaria, '
            'pero dentro de cada modalidad el ingreso es prácticamente plano (en línea ~7,1–7,5 M y en física '
            '~2,7–2,8 M, sin relación con la escolaridad). La educación funciona como boleto de entrada al '
            'trabajo en línea, no como generador directo de ingreso. En paralelo, trabajar más horas no mejora '
            'la tarifa real: en física la tarifa cae de 4,31 a 2,82 USD/h al pasar de <30 h a >56 h, y la '
            'cotización a pensión es mínima precisamente entre quienes dependen al 100% de la aplicación '
            '(32,6% cotiza), configurando un perfil de vulnerabilidad multidimensional.'
        ),
        'limitacion': (
            'Las combinaciones con pocas observaciones (por ejemplo, Primaria en línea, n=32) generan promedios '
            'poco robustos. El análisis identifica asociaciones y patrones de composición, pero no establece '
            'causalidad: no puede afirmarse que la educación cause el acceso a la modalidad en línea ni que las '
            'horas causen la caída de la tarifa. No se controla por experiencia previa, antigüedad o capital inicial.'
        ),
        'decision': (
            'Diseñar programas de reconversión centrados en el acceso a la modalidad en línea (no solo en la '
            'titulación), dado que la educación solo rinde en ese segmento; y establecer topes algorítmicos de '
            'jornada para frenar la autoexplotación, protegiendo a los dependientes exclusivos en plataformas '
            'físicas, que combinan las jornadas más largas (52–53 h) con la menor cotización (32,6%).'
        ),
    }


def _conocimientos_vista4():
    """Dos conocimientos multidimensionales de la Vista 4 (estructura de 8 campos)."""
    return [
        {
            'id': 'KM-4.1',
            'titulo': 'El premio por educación es un efecto de composición, no un retorno directo',
            'pregunta': '¿La educación superior incrementa el ingreso neto dentro de cada modelo de plataforma?',
            'dimensiones_medidas': 'dim_trabajador.nivel_educativo × dim_plataforma.tipo_plataforma; medida = '
                                   'ingreso_neto_mensual_cop (promedio aritmético).',
            'procedimiento': 'Roll-up (3 grupos formativos: Básica / Técnica / Superior) → Drill-down '
                             '(5 niveles educativos), cruzado con tipo_plataforma. Promedios recalculados por '
                             'celda de la matriz.',
            'evidencia': 'Visualización 1 y matriz nivel educativo × modelo de plataforma.',
            'hallazgo': 'En el agregado hay un gradiente de 2,1x (Posgrado 6.545.561 vs Primaria 3.058.687 COP). '
                        'Al desagregar por modalidad el gradiente desaparece: en línea el ingreso es plano '
                        '(Secundaria 7.469.910, Técnico 7.296.951, Universitario 7.128.394, Posgrado 7.234.574 '
                        'COP, rango <5%) y en física también (2.657.234 a 2.823.820 COP).',
            'interpretacion': 'Corrige el hallazgo K4.1: no existe "retorno exponencial" en la nube. La educación '
                             'no premia por sí misma; su efecto agregado proviene de que los más educados se '
                             'concentran en la modalidad en línea, mejor pagada. El título actúa como boleto de '
                             'entrada, no como multiplicador de ingreso.',
            'utilidad': 'Orienta la política hacia programas de acceso a la modalidad en línea y reconversión, '
                        'en lugar de promover únicamente la titulación formal.',
            'limitacion': 'Algunas celdas tienen muestras pequeñas (Primaria en línea, n=32), por lo que sus '
                          'promedios no son robustos; no se controla por experiencia ni antigüedad.',
        },
        {
            'id': 'KM-4.2',
            'titulo': 'Doble trampa: a más horas y más dependencia, menor tarifa y menor cotización',
            'pregunta': '¿El perfil de mayor vulnerabilidad combina jornadas extremas, dependencia exclusiva y '
                        'desprotección pensional?',
            'dimensiones_medidas': 'dim_trabajador (dependencia_ingresos, afiliacion_pension) × horas_semanales '
                                   'y tipo_plataforma; medidas = ingreso_neto_hora_usd y cotización.',
            'procedimiento': 'Agrupación por banda de jornada (5 bandas) × tipo de plataforma; proporción de '
                             'cotizantes con denominador = total de cada grupo de dependencia.',
            'evidencia': 'Visualización 2 e indicador 3.',
            'hallazgo': 'En plataformas físicas la tarifa por hora cae de 4,31 USD/h (<30 h) a 2,82 USD/h '
                        '(>56 h), devaluando la hora marginal. Solo el 32,6% de los dependientes exclusivos '
                        'cotiza a pensión (2.060 de 6.324), frente al 40,7% de los de fuente complementaria '
                        '(985 de 2.419). Entre los dependientes exclusivos en física, el 73,4% (3.579 de 4.879) '
                        'no cotiza.',
            'interpretacion': 'Profundiza K4.2 y K4.3: la autoexplotación horaria no eleva la tarifa real y '
                             'convive con la mayor desprotección. Quien más depende de la aplicación es quien '
                             'menos protección de vejez acumula, cerrando un círculo de vulnerabilidad.',
            'utilidad': 'Sustenta la desconexión algorítmica y un piso de microaportes a seguridad social '
                        'vinculado a cada entrega o carrera completada.',
            'limitacion': 'Es una asociación observada, no causal: no se demuestra que las horas causen la caída '
                          'de la tarifa ni que la dependencia cause la no cotización (pueden mediar ingresos '
                          'insuficientes).',
        },
    ]
