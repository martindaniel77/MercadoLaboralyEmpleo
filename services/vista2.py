"""
Vista 2 — Comparación de Grupos y Territorios.

Pregunta: ¿Existen diferencias significativas en los ingresos, las tarifas por
hora y las condiciones laborales entre países, géneros y modelos de plataforma?
"""

from services.common import (
    COLOR_TIPO_PLATAFORMA,
    GENEROS,
    TIPOS_PLATAFORMA,
    _cop,
    _pct,
    _run,
    _usd,
)


def _fmt_celda(v):
    """Formatea una celda de la matriz (tarifa USD/h) o devuelve guion si no hay datos."""
    if v is None:
        return '—'
    return _usd(float(v))


def get_vista2(filtros=None):
    """Retorna todos los datos de la Vista 2 (Comparación de Grupos y Territorios).

    Filtros soportados (operaciones Slice/Dice):
      - tipo   : valor de dim_plataforma.tipo_plataforma o 'Todos'
      - genero : valor de dim_trabajador.genero o 'Todos'
      - nivel  : 'pais' (Roll-up) o 'departamento' (Drill-down) de la jerarquía
                 dim_geografia.pais -> departamento_region
      - pivot  : 'pais_tipo' o 'tipo_pais' (operación Pivot de la matriz)
    """
    filtros = dict(filtros or {})
    filtros.setdefault('tipo', 'Todos')
    filtros.setdefault('genero', 'Todos')
    filtros.setdefault('nivel', 'pais')
    filtros.setdefault('pivot', 'pais_tipo')

    conds = []
    params = {}
    if filtros.get('tipo') and filtros['tipo'] != 'Todos':
        conds.append('p.tipo_plataforma = :tipo')
        params['tipo'] = filtros['tipo']
    if filtros.get('genero') and filtros['genero'] != 'Todos':
        conds.append('t.genero = :genero')
        params['genero'] = filtros['genero']
    where = (' WHERE ' + ' AND '.join(conds)) if conds else ''

    _FROM = (
        'FROM fact_gig_economy f '
        'JOIN dim_plataforma p ON p.id_plataforma = f.id_plataforma '
        'JOIN dim_trabajador t ON t.id_trabajador = f.id_trabajador '
        'JOIN dim_geografia g ON g.id_geografia = f.id_geografia'
    )

    # ---- Universo ----
    total = _run(f'SELECT COUNT(DISTINCT f.id_trabajador) {_FROM}{where}', params)[0][0]

    # ---- Indicadores (KPIs) ----
    ingreso_neto = _run(
        f'SELECT AVG(f.ingreso_neto_mensual_cop) {_FROM}{where}', params)[0][0]
    tarifa = _run(
        f'SELECT AVG(f.ingreso_neto_hora_usd) {_FROM}{where}', params)[0][0]
    desprotegidos = _run(
        f"SELECT COUNT(DISTINCT f.id_trabajador) {_FROM}{where} AND "
        "t.afiliacion_pension = 'No cotiza' AND t.cuenta_con_arl = 'No (Sin cobertura ARL)'",
        params,
    )[0][0]

    kpis = [
        {
            'valor': '$' + _cop(ingreso_neto),
            'unidad': 'COP / mes',
            'label': 'Ingreso neto mensual promedio',
            'sub': 'Media aritmética de ingreso_neto_mensual_cop',
        },
        {
            'valor': _usd(tarifa) + ' USD/h',
            'unidad': 'USD / hora',
            'label': 'Tarifa neta promedio por hora',
            'sub': 'Media aritmética de ingreso_neto_hora_usd',
        },
        {
            'valor': f'{_pct(desprotegidos, total)}%'.replace('.', ','),
            'unidad': f'{_cop(desprotegidos)}' + ' trabajadores',
            'label': 'Sin protección social',
            'sub': 'Sin cotización a pensión y sin cobertura ARL',
        },
    ]

    # ---- Viz 1: tarifa por territorio (Drill-down / Roll-up) ----
    if filtros['nivel'] == 'departamento':
        geo_rows = _run(
            'SELECT g.departamento_region, g.pais, '
            f'AVG(f.ingreso_neto_hora_usd), COUNT(DISTINCT f.id_trabajador) '
            f'{_FROM}{where} '
            'GROUP BY g.departamento_region, g.pais '
            'ORDER BY AVG(f.ingreso_neto_hora_usd) DESC',
            params,
        )
        barras = [
            {
                'label': (f'{dep} (Colombia)' if pais == 'Colombia' else f'{dep} ({pais})'),
                'value': float(v),
                'display': _usd(float(v)) + ' USD/h',
                'color': '#edbd4c' if pais == 'Colombia' else '#3e7cb1',
            }
            for dep, pais, v, _n in geo_rows
        ]
        geo_titulo = 'Tarifa neta promedio por hora (USD) por departamento / región'
        geo_subtitulo = 'Drill-down: de país a departamento_region (Colombia en dorado)'
    else:
        geo_rows = _run(
            'SELECT g.pais, AVG(f.ingreso_neto_hora_usd), COUNT(DISTINCT f.id_trabajador) '
            f'{_FROM}{where} GROUP BY g.pais '
            'ORDER BY AVG(f.ingreso_neto_hora_usd) DESC',
            params,
        )
        barras = [
            {
                'label': pais,
                'value': float(v),
                'display': _usd(float(v)) + ' USD/h',
                'color': '#3e7cb1',
            }
            for pais, v, _n in geo_rows
        ]
        geo_titulo = 'Tarifa neta promedio por hora (USD) por país'
        geo_subtitulo = 'Roll-up: nivel superior de la jerarquía geográfica'

    viz1 = {
        'titulo': geo_titulo,
        'subtitulo': geo_subtitulo,
        'nivel': filtros['nivel'],
        'barras': barras,
        'max': max((b['value'] for b in barras), default=1.0),
    }

    # ---- Viz 2: ingreso neto mensual por género x tipo de plataforma ----
    gx_rows = _run(
        'SELECT t.genero, p.tipo_plataforma, AVG(f.ingreso_neto_mensual_cop) '
        f'{_FROM}{where} GROUP BY t.genero, p.tipo_plataforma',
        params,
    )
    gx_barras = []
    for genero, tipo, v in sorted(gx_rows, key=lambda r: float(r[2]), reverse=True):
        gx_barras.append({
            'label': f'{genero} — {tipo}',
            'value': float(v),
            'display': '$' + _cop(float(v)) + ' COP',
            'color': COLOR_TIPO_PLATAFORMA.get(tipo, '#b8a886'),
        })
    viz2 = {
        'titulo': 'Ingreso neto mensual promedio por género y modelo de plataforma',
        'subtitulo': 'La modalidad (física vs en línea) domina sobre el género',
        'barras': gx_barras,
        'max': max((b['value'] for b in gx_barras), default=1.0),
    }

    # ---- Matriz: país x tipo de plataforma (tarifa USD/h) ----
    m_rows = _run(
        'SELECT g.pais, p.tipo_plataforma, AVG(f.ingreso_neto_hora_usd) '
        f'{_FROM}{where} GROUP BY g.pais, p.tipo_plataforma',
        params,
    )
    m = {}
    for pais, tipo, v in m_rows:
        m[(pais, tipo)] = float(v)

    paises_orden = [b['label'] for b in barras] if filtros['nivel'] == 'pais' else \
        [r[0] for r in _run(
            f'SELECT g.pais {_FROM}{where} GROUP BY g.pais '
            'ORDER BY AVG(f.ingreso_neto_hora_usd) DESC', params)]

    if filtros['pivot'] == 'pais_tipo':
        filas = paises_orden
        columnas = TIPOS_PLATAFORMA
        cells = [[_fmt_celda(m.get((f, c))) for c in columnas] for f in filas]
    else:
        filas = TIPOS_PLATAFORMA
        columnas = paises_orden
        cells = [[_fmt_celda(m.get((c, f))) for c in columnas] for f in filas]

    matriz = {
        'filas': filas,
        'columnas': columnas,
        'cells': cells,
        'pivot': filtros['pivot'],
        'medida': 'ingreso_neto_hora_usd (promedio)',
    }

    return {
        'titulo': 'Comparación de Grupos y Territorios',
        'pregunta': '¿Existen diferencias significativas en los ingresos, las tarifas por hora y las '
                    'condiciones laborales entre países, géneros y modelos de plataforma?',
        'dimensiones': [
            {'nombre': 'dim_geografia', 'atributos': 'pais, departamento_region'},
            {'nombre': 'dim_trabajador', 'atributos': 'genero, afiliacion_pension, cuenta_con_arl'},
            {'nombre': 'dim_plataforma', 'atributos': 'tipo_plataforma'},
        ],
        'medidas': [
            {'nombre': 'Ingreso neto mensual', 'formula': 'AVG(ingreso_neto_mensual_cop)',
             'agregacion': 'Promedio aritmético (recalculado al cambiar el nivel de agrupación)'},
            {'nombre': 'Tarifa neta por hora', 'formula': 'AVG(ingreso_neto_hora_usd)',
             'agregacion': 'Promedio aritmético'},
            {'nombre': 'Desprotección social', 'formula': 'COUNT DISTINCT (sin pensión y sin ARL) / total',
             'agregacion': 'Proporción (denominador = trabajadores del subconjunto)'},
        ],
        'jerarquias': [
            {'nombre': 'Jerarquía geográfica',
             'ruta': 'pais → departamento_region → ciudad_municipio',
             'operaciones': 'Drill-down / Roll-up'},
        ],
        'filtros': {
            'tipo': {'opciones': TIPOS_PLATAFORMA, 'seleccion': filtros['tipo']},
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
            'tipo': filtros['tipo'],
            'genero': filtros['genero'],
            'nivel': filtros['nivel'],
            'pivot': filtros['pivot'],
        },
        'conocimientos': _conocimientos_vista2(),
        'interpretacion': (
            'Los ingresos y las tarifas dependen de la geografía y de la modalidad de plataforma '
            'mucho más que del género. La tarifa horaria varía 9,6 veces entre Estados Unidos '
            '(26,21 USD/h) y Colombia (2,73 USD/h), y la desprotección social en Colombia (72,7% sin '
            'pensión ni ARL) duplica la del resto de países (29–35%). El cruce de género y modalidad '
            'revela que las diferencias salariales agregadas por género son un efecto de composición: '
            'las mujeres, sobrerrepresentadas en el trabajo en línea mejor pagado, registran promedios '
            'superiores, pero dentro de cada modalidad la brecha horaria es inferior al 4%. Las '
            'condiciones laborales son más duras en el trabajo físico: 52,8 h/semana y 69,1% de '
            'desprotección, frente a 34,1 h y 37,4% en línea.'
        ),
        'limitacion': (
            'La comparación internacional usa la tarifa en USD sin ajustar por paridad de poder '
            'adquisitivo, por lo que 2,73 USD en Colombia adquieren más bienes locales que en Estados '
            'Unidos. Además, los países extranjeros solo cuentan con una región/ciudad representada, lo '
            'que impide contrastar su dispersión subnacional; y los promedios no controlan por variables '
            'omitidas como experiencia, antigüedad o capital inicial.'
        ),
        'decision': (
            'Impulsar un mecanismo de microaportes automáticos a seguridad social por cada carrera o '
            'entrega completada, focalizado en Colombia (5.777 trabajadores sin pensión ni ARL, el 72,7% '
            'de su población de plataformas), y complementar con políticas de equidad orientadas a ampliar '
            'el acceso de las mujeres a las modalidades en línea mejor remuneradas, donde su participación '
            'aún es del 38,0%.'
        ),
    }


def _conocimientos_vista2():
    """Dos conocimientos multidimensionales de la Vista 2 (estructura de 8 campos)."""
    return [
        {
            'id': 'KM-2.1',
            'titulo': 'Brecha geográfica de 9,6x con dispersión subnacional nula en Colombia',
            'pregunta': '¿La disparidad de tarifas por hora es un fenómeno internacional o también se '
                        'reproduce al interior de Colombia?',
            'dimensiones_medidas': 'dim_geografia.pais y departamento_region; medida = '
                                   'ingreso_neto_hora_usd (promedio aritmético).',
            'procedimiento': 'Roll-up (agrupación por país, 8 grupos) → Drill-down (agrupación por '
                             'departamento_region, 15 grupos). Promedio de tarifa USD/h recalculado en '
                             'cada nivel de la jerarquía geográfica.',
            'evidencia': 'Visualización 1 (barras por país y por departamento/región).',
            'hallazgo': 'En el nivel país, un trabajador de Estados Unidos gana 26,21 USD/h frente a '
                        '2,73 USD/h en Colombia (9,6x). Al hacer drill-down, los 8 departamentos '
                        'colombianos se agrupan en un rango estrecho de 2,65 a 2,89 USD/h, mientras los '
                        'demás países quedan representados por una única ciudad. Ningún territorio '
                        'colombiano escapa a la tarifa baja.',
            'interpretacion': 'Profundiza el hallazgo K2.1: la desventaja de Colombia es estructural a '
                             'escala nacional y no presenta bolsillos regionales de alto valor. La brecha '
                             'respondería a factores macro (tipo de cambio, poder adquisitivo, estructura '
                             'de demanda) más que a dinámicas locales.',
            'utilidad': 'Justifica un piso tarifario nacional indexado al salario mínimo antes que '
                        'intervenciones territoriales aisladas.',
            'limitacion': 'La comparación en USD no ajusta por paridad de poder adquisitivo y los países '
                          'extranjeros solo tienen una ciudad representada, por lo que no puede afirmarse '
                          'que su dispersión subnacional sea inexistente.',
        },
        {
            'id': 'KM-2.2',
            'titulo': 'La brecha salarial de género se disuelve al controlar por modalidad',
            'pregunta': '¿Ganan menos las mujeres que los hombres en la Gig Economy?',
            'dimensiones_medidas': 'dim_trabajador.genero × dim_plataforma.tipo_plataforma; medidas = '
                                   'ingreso_neto_mensual_cop e ingreso_neto_hora_usd (promedios).',
            'procedimiento': 'Comparación de promedios en dos niveles de agrupación: agregado por género '
                             'y desagregado por género × modalidad. Se recalculan los promedios al cambiar '
                             'el nivel (condición de no sumar/arrastrar promedios).',
            'evidencia': 'Visualización 2 e indicadores 1 y 2.',
            'hallazgo': 'A nivel agregado las mujeres ganan más por hora (7,78 vs 5,74 USD/h, +35,5%) y '
                        'por mes (4.931.092 vs 4.029.633 COP). Pero al desagregar por modalidad la '
                        'diferencia casi desaparece: en plataformas físicas la mujer gana 2,95 vs 3,06 '
                        'USD/h (−3,6%) y en línea 12,69 vs 12,56 USD/h (+1,0%). La ventaja agregada se '
                        'debe a que el 49,6% de las mujeres trabaja en línea frente al 28,2% de los hombres.',
            'interpretacion': 'Es un efecto de composición (paradoja de Simpson), no evidencia de ventaja '
                             'femenina. Confirma que la segregación por modalidad —y no la discriminación '
                             'directa— explica las diferencias agregadas de remuneración; dentro de cada '
                             'modalidad la igualdad salarial por hora es casi total.',
            'utilidad': 'Redirige la política de equidad desde "igualar salarios" hacia "ampliar el acceso '
                        'de las mujeres a las modalidades en línea mejor remuneradas y reducir la segregación".',
            'limitacion': 'No se controla por horas de cuidado no remunerado ni por experiencia; la '
                          'igualdad dentro de modalidad no descarta diferencias en acceso a proyectos de '
                          'mayor valor o en trayectorias de promoción.',
        },
    ]
