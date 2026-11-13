"""
Servicio de Datos y Metadatos para la Etapa 6: Conocimiento Oculto con Orange Data Mining.
Contiene la caracterización técnica, métricas de evaluación de modelos supervisados,
parámetros de clustering k-Means, resultados de Text Mining (LDA / Word Cloud)
y las fichas estructuradas de Conocimiento Oculto extraídas del pipeline Orange3.
"""

# Resumen metodológico general del flujo de Orange
METODOLOGIA_ORANGE = {
    'herramienta': 'Orange Data Mining v3.40.0 (x86_64)',
    'archivo_flujo': 'GIG ECONOMY.ows',
    'dataset_origen': 'dataset_gig_economy_tratado.csv (12.350 registros, 27 variables)',
    'particion_datos': '10-Fold Cross-Validation Estratificado para modelos supervisados',
    'semilla_aleatoria': 'Replicable / Deterministic sampling activo',
    'secciones': [
        {
            'id': 'supervisado',
            'nombre': 'Aprendizaje Supervisado · Clasificación Pensional',
            'objetivo': 'Predecir la condición de cotización activa a pensión e identificar los factores determinantes de la protección social formal.',
            'modelos': ['Classification Tree', 'Random Forest (100 árboles)', 'Logistic Regression (Ridge L2)'],
            'variable_objetivo': 'afiliacion_pension (Binaria: Cotiza activamente / No cotiza)'
        },
        {
            'id': 'clustering',
            'nombre': 'Aprendizaje No Supervisado · Segmentación de Vulnerabilidad',
            'objetivo': 'Descubrir agrupamientos naturales de trabajadores a partir de condiciones laborales y financieras objetivas.',
            'algoritmo': 'k-Means con k=3 clusters y estandarización Z-score',
            'variables_clave': ['ingreso_neto_hora_usd', 'horas_semanales', 'edad', 'ingreso_bruto_mensual_cop', 'costos_operativos_mensuales_cop']
        },
        {
            'id': 'texto',
            'nombre': 'Minería de Texto · Percepción Social en YouTube',
            'objetivo': 'Contrastar la evidencia estadística con el discurso empírico de trabajadores en comunidades digitales.',
            'corpus': '242 comentarios depurados extraídos con YouTube Data API v3 (Video: OXT8xdqcAoU)',
            'tecnicas': ['Topic Modelling (Latent Dirichlet Allocation - 7 Tópicos)', 'Word Cloud TF-IDF', 'Clustering Textual']
        }
    ]
}

# ---------------------------------------------------------------------------
# SECCIÓN 1: APRENDIZAJE SUPERVISADO
# ---------------------------------------------------------------------------
SUPERVISADO_DATA = {
    'variable_target': 'afiliacion_pension',
    'clases': [
        {'nombre': 'Cotiza activamente', 'total': 4352, 'porcentaje': 35.24},
        {'nombre': 'No cotiza', 'total': 7998, 'porcentaje': 64.76}
    ],
    'total_instancias': 12350,
    'estrategia': '10-Fold Cross Validation Estratificado (Evaluación sobre 12.350 casos)',
    'modelos_evaluacion': [
        {
            'nombre': 'Random Forest',
            'tipo': 'Ensamble Bagging (100 árboles)',
            'auc': 0.833,
            'ca': 0.749,
            'f1': 0.743,
            'precision': 0.742,
            'recall': 0.749,
            'mcc': 0.432,
            'matriz': {
                'vp_cotiza': 2457, 'fn_cotiza': 1895,
                'fp_nocotiza': 1209, 'vn_nocotiza': 6789,
                'total_aciertos': 9246, 'tasa_acierto_pct': 74.87,
                'sensibilidad_cotiza': 56.46, 'especificidad_nocotiza': 84.88
            },
            'destacado': True
        },
        {
            'nombre': 'Classification Tree',
            'tipo': 'Árbol de Decisión Binario (Max depth 5, Min leaf 15)',
            'auc': 0.831,
            'ca': 0.743,
            'f1': 0.738,
            'precision': 0.737,
            'recall': 0.743,
            'mcc': 0.420,
            'matriz': {
                'vp_cotiza': 2436, 'fn_cotiza': 1916,
                'fp_nocotiza': 1257, 'vn_nocotiza': 6741,
                'total_aciertos': 9177, 'tasa_acierto_pct': 74.31,
                'sensibilidad_cotiza': 55.97, 'especificidad_nocotiza': 84.28
            },
            'destacado': False
        },
        {
            'nombre': 'Logistic Regression',
            'tipo': 'Modelo Lineal Generalizado (Ridge L2, C=1.0)',
            'auc': 0.783,
            'ca': 0.720,
            'f1': 0.699,
            'precision': 0.711,
            'recall': 0.720,
            'mcc': 0.345,
            'matriz': {
                'vp_cotiza': 1760, 'fn_cotiza': 2592,
                'fp_nocotiza': 868, 'vn_nocotiza': 7130,
                'total_aciertos': 8890, 'tasa_acierto_pct': 71.98,
                'sensibilidad_cotiza': 40.44, 'especificidad_nocotiza': 89.15
            },
            'destacado': False
        }
    ],
    'comparacion_roc_pvalues': [
        {'fila': 'Tree', 'vs_rf': 0.665, 'vs_lr': 0.967},
        {'fila': 'Random Forest', 'vs_tree': 0.335, 'vs_lr': 0.956},
        {'fila': 'Logistic Regression', 'vs_tree': 0.033, 'vs_rf': 0.044}
    ],
    'ranking_variables': [
        {'pos': 1, 'variable': 'cuenta_con_arl', 'tipo': 'Categórica', 'gain_ratio': 0.160, 'gini': 0.082, 'rol': 'Determinante crítico primario'},
        {'pos': 2, 'variable': 'tipo_plataforma', 'tipo': 'Categórica', 'gain_ratio': 0.048, 'gini': 0.029, 'rol': 'Segmentación estructural físico vs nube'},
        {'pos': 3, 'variable': 'ingreso_neto_hora_usd', 'tipo': 'Numérica', 'gain_ratio': 0.028, 'gini': 0.035, 'rol': 'Poder adquisitivo estandarizado'},
        {'pos': 4, 'variable': 'ingreso_neto_mensual_cop', 'tipo': 'Numérica', 'gain_ratio': 0.025, 'gini': 0.031, 'rol': 'Retorno monetario local neto'},
        {'pos': 5, 'variable': 'nivel_territorial', 'tipo': 'Categórica', 'gain_ratio': 0.023, 'gini': 0.023, 'rol': 'Escala de análisis regional vs global'},
        {'pos': 6, 'variable': 'pais', 'tipo': 'Categórica', 'gain_ratio': 0.019, 'gini': 0.023, 'rol': 'Estructura regulatoria por país'},
        {'pos': 7, 'variable': 'categoria_servicio', 'tipo': 'Categórica', 'gain_ratio': 0.019, 'gini': 0.029, 'rol': 'Ocupación desarrollada'},
        {'pos': 8, 'variable': 'ingreso_bruto_mensual_cop', 'tipo': 'Numérica', 'gain_ratio': 0.017, 'gini': 0.022, 'rol': 'Facturación antes de costos'},
        {'pos': 9, 'variable': 'afiliacion_salud', 'tipo': 'Categórica', 'gain_ratio': 0.012, 'gini': 0.003, 'rol': 'Régimen de salud (Contributivo/Subsidiado)'},
        {'pos': 10, 'variable': 'horas_semanales', 'tipo': 'Numérica', 'gain_ratio': 0.008, 'gini': 0.010, 'rol': 'Intensidad de jornada laboral'},
        {'pos': 11, 'variable': 'nivel_educativo', 'tipo': 'Categórica', 'gain_ratio': 0.007, 'gini': 0.008, 'rol': 'Capital humano formal'},
        {'pos': 12, 'variable': 'costos_operativos_mensuales_cop', 'tipo': 'Numérica', 'gain_ratio': 0.002, 'gini': 0.003, 'rol': 'Presión financiera operativa'},
        {'pos': 13, 'variable': 'dependencia_ingresos', 'tipo': 'Categórica', 'gain_ratio': 0.002, 'gini': 0.002, 'rol': 'Exclusividad económica'},
        {'pos': 14, 'variable': 'genero', 'tipo': 'Categórica', 'gain_ratio': 0.001, 'gini': 0.001, 'rol': 'Identidad de género'},
        {'pos': 15, 'variable': 'edad', 'tipo': 'Numérica', 'gain_ratio': 0.001, 'gini': 0.001, 'rol': 'Edad biológica'},
        {'pos': 16, 'variable': 'calificacion_promedio_app', 'tipo': 'Numérica', 'gain_ratio': 0.000, 'gini': 0.001, 'rol': 'Reputación algorítmica'},
        {'pos': 17, 'variable': 'antiguedad_meses', 'tipo': 'Numérica', 'gain_ratio': 0.000, 'gini': 0.000, 'rol': 'Tiempo en la plataforma'}
    ]
}

# ---------------------------------------------------------------------------
# SECCIÓN 2: CLUSTERING NO SUPERVISADO
# ---------------------------------------------------------------------------
CLUSTERING_DATA = {
    'metodo': 'k-Means con distancia Euclídea sobre variables normalizadas (Z-Score)',
    'k_seleccionado': 3,
    'silhouette_medio': 0.12,
    'chi_cuadrado_pension': {
        'estadistico': 553.07,
        'p_value': 0.000,
        'grados_libertad': 2,
        'interpretacion': 'Diferencia de protección social entre clusters estadísticamente significativa al 99.9% de confianza.'
    },
    'clusters': [
        {
            'id': 'C1',
            'nombre': 'Núcleo de Precarización y Trabajo Físico de Subsistencia',
            'pct_cotiza': 28.0,
            'pct_no_cotiza': 72.0,
            'perfil': 'Trabajadores con sobrecarga horaria en plataformas físicas (reparto y transporte), baja tarifa horaria promedio y altísima desprotección social (7 de cada 10 no cotizan a pensión ni tienen ARL).',
            'tamano_aprox': 'Mayoritaria en escala regional/Colombia',
            'color': '#ef4444'
        },
        {
            'id': 'C2',
            'nombre': 'Freelancers y Especialistas Digitales en la Nube',
            'pct_cotiza': 49.0,
            'pct_no_cotiza': 51.0,
            'perfil': 'Trabajadores de desarrollo de software, diseño y asesoría profesional con tarifas horarias en USD sustancialmente más altas, menor carga horaria semanal y paridad en la cotización pensional.',
            'tamano_aprox': 'Segmento medio altamente calificado',
            'color': '#3b82f6'
        },
        {
            'id': 'C3',
            'nombre': 'Trabajadores Mixtos y de Transición Ocupacional',
            'pct_cotiza': 50.0,
            'pct_no_cotiza': 50.0,
            'perfil': 'Perfiles de jornada complementaria o servicios del hogar, con balance intermedio de horas e ingresos que utilizan las apps como red de seguridad económica transitoria.',
            'tamano_aprox': 'Segmento intermedio de choque económico',
            'color': '#10b981'
        }
    ]
}

# ---------------------------------------------------------------------------
# SECCIÓN 3: MINERÍA DE TEXTO Y PERCEPCIÓN EN YOUTUBE
# ---------------------------------------------------------------------------
TEXT_MINING_DATA = {
    'video_id': 'OXT8xdqcAoU',
    'video_url': 'https://www.youtube.com/watch?v=OXT8xdqcAoU',
    'titulo_video': 'The Gig Economy & Future of Work (Documental / Debate Global)',
    'comentarios_descargados': 262,
    'comentarios_analizados': 242,
    'tokens_totales': 1027,
    'vocabulario_unico': 100,
    'algoritmo_topicos': 'Latent Dirichlet Allocation (LDA)',
    'numero_topicos': 7,
    'log_perplexity': 31.53162,
    'topic_coherence': 0.40812,
    'topicos': [
        {
            'numero': 1,
            'palabras': 'gig, video, economy, freelance, work, working, people, freelancing, way, health',
            'eje': 'Impacto macroeconómico y salud del trabajador',
            'descripcion': 'Debate sobre la economía gig, la salud y la condición del trabajador independiente.'
        },
        {
            'numero': 2,
            'palabras': 'ted, music, wef, freelancing, videos, background, head, thank, sure, app',
            'eje': 'Debate institucional y rol de las aplicaciones',
            'descripcion': 'Reacciones a la postura del Foro Económico Mundial (WEF) y aplicaciones de intermediación.'
        },
        {
            'numero': 3,
            'palabras': 'good, freelancing, job, work, business, get, like, clients, money, much',
            'eje': 'Modelo de negocio freelance y monetización',
            'descripcion': 'Gestión de clientes, cobro de honorarios y rendimiento económico del trabajo autónomo.'
        },
        {
            'numero': 4,
            'palabras': 'get, freelance, animation, one, job, freelancer, years, freelancing, make, thanks',
            'eje': 'Trayectoria profesional y experiencia acumulada',
            'descripcion': 'Testimonios de profesionales creativos e informáticos a lo largo de los años en plataformas.'
        },
        {
            'numero': 5,
            'palabras': 'people, real, want, see, day, guess, life, still, offers, got',
            'eje': 'Realidad cotidiana vs promesas de flexibilidad',
            'descripcion': 'Disonancia entre la narrativa de "libertad" y el día a día de las ofertas de trabajo.'
        },
        {
            'numero': 6,
            'palabras': 'like, work, get, pay, better, think, people, good, day, market',
            'eje': 'Calidad de remuneración y dinámicas del mercado',
            'descripcion': 'Exigencia de mejores tarifas, pagos justos por jornada y funcionamiento del mercado laboral.'
        },
        {
            'numero': 7,
            'palabras': 'forum, economic, world, soundtrack, videos, happy, give, amazing, think, made',
            'eje': 'Perspectiva sociopolítica global del empleo futuro',
            'descripcion': 'Discusión global sobre el rumbo económico internacional y la precarización contemporánea.'
        }
    ],
    'top_palabras_nube': [
        {'palabra': 'freelancing', 'peso': 47},
        {'palabra': 'work', 'peso': 33},
        {'palabra': 'get', 'peso': 29},
        {'palabra': 'job', 'peso': 29},
        {'palabra': 'gig', 'peso': 27},
        {'palabra': 'people', 'peso': 23},
        {'palabra': 'good', 'peso': 23},
        {'palabra': 'ted', 'peso': 23},
        {'palabra': 'freelance', 'peso': 22},
        {'palabra': 'video', 'peso': 22},
        {'palabra': 'economy', 'peso': 19},
        {'palabra': 'like', 'peso': 19},
        {'palabra': 'world', 'peso': 19},
        {'palabra': 'money', 'peso': 17},
        {'palabra': 'business', 'peso': 16},
        {'palabra': 'clients', 'peso': 15},
        {'palabra': 'health', 'peso': 14},
        {'palabra': 'insurance', 'peso': 12},
        {'palabra': 'pay', 'peso': 12},
        {'palabra': 'hours', 'peso': 11}
    ],
    'comentario_emblematico': {
        'texto_original': "It's as you said Ted Ed, freelancing is definitely a good support net for quick money. It's safe for part timers, but maybe not in the long run.",
        'fecha': '2022-09-01T15:07:08Z',
        'likes': 539,
        'cluster_asignado': 'C3',
        'silhouette': 0.50,
        'interpretacion': 'Sintetiza la paradoja central: la plataforma es útil como ingreso de emergencia para estudiantes o part-timers, pero insostenible como proyecto de vida por falta de seguridad social a largo plazo.'
    }
}

# ---------------------------------------------------------------------------
# CATÁLOGO DE CONOCIMIENTOS OCULTOS (FICHAS ESTRUCTURADAS)
# ---------------------------------------------------------------------------
CONOCIMIENTOS_OCULTOS = [
    {
        'codigo': 'KO-1.1',
        'seccion': 'Aprendizaje Supervisado',
        'titulo': 'La ARL como condicionante no lineal de la cotización pensional',
        'resumen': 'Tener cobertura de ARL multiplica exponencialmente la probabilidad de cotizar a pensión (Gain Ratio 0.160), constituyendo el nodo raíz absoluto del árbol de clasificación.',
        'pregunta': '¿Qué factores explican y predicen con mayor fidelidad si un trabajador de la economía gig cotiza activamente a pensión?',
        'variables': 'cuenta_con_arl, tipo_plataforma, ingreso_neto_hora_usd, afiliacion_salud vs afiliacion_pension',
        'procedimiento': 'Algoritmo de ganancia de información (Gain Ratio y Gini) en Orange sobre 17 predictoras tras validación cruzada estratificada 10-Fold.',
        'evidencia': 'El widget Rank asigna a cuenta_con_arl un Gain Ratio de 0.160 (el triple que tipo_plataforma con 0.048). En el Tree Viewer, la regla cuenta_con_arl = Si en escala Nacional/Regional produce 100% de cotización (941 de 941 registros).',
        'hallazgo': 'La afiliación a pensión no es una decisión aislada ni dependiente primariamente del ingreso, sino que está supeditada al vínculo formal con riesgos laborales (ARL). Quien no tiene ARL cae en un 92.8% de no cotización en trabajo físico.',
        'interpretacion': 'Confirma la "formalidad en bloque": los trabajadores independientes no cotizan parcialmente; o bien entran al esquema integral (Salud + Pensión + ARL) o quedan 100% al margen.',
        'utilidad': 'Las políticas que intentan incentivar la pensión bajando tarifas fracasan si no resuelven la obligatoriedad y subsidio inicial al aseguramiento de riesgos laborales (ARL).',
        'limitacion': 'Asociación predictiva derivada de encuestas con marco normativo vigente; un cambio legal en aportes independientes podría alterar la dependencia del nodo raíz.'
    },
    {
        'codigo': 'KO-1.2',
        'seccion': 'Aprendizaje Supervisado',
        'titulo': 'Superioridad de ensamble Random Forest y asimetría de la Regresión Logística',
        'resumen': 'Random Forest supera consistentemente al modelo lineal (AUC 0.833 vs 0.783, p=0.956), revelando que las decisiones laborales obedecen a umbrales interactivos no lineales.',
        'pregunta': '¿Se comporta la decisión de cotizar como una probabilidad lineal aditiva o requiere estructuras no lineales de ensamble?',
        'variables': '17 predictoras continuas y categóricas evaluadas sobre afiliacion_pension',
        'procedimiento': 'Comparación de AUC, F1-Score, Matriz de Confusión y prueba de hipótesis sobre curvas ROC en Test and Score (10 Folds).',
        'evidencia': 'Random Forest alcanza AUC 0.833 y F1 0.743 frente a Logistic Regression (AUC 0.783, F1 0.699). La matriz de confusión muestra que la regresión logística genera 2.592 falsos negativos (omite al 59.6% de los cotizantes).',
        'hallazgo': 'La regresión logística asume linealidad aditiva y subestima gravemente a los cotizantes reales. Random Forest captura las complejas interacciones entre horas trabajadas, modalidad en línea y costos fijos.',
        'interpretacion': 'Las dinámicas socioeconómicas del trabajo digital no operan con gradientes suaves: existen "saltos discretos" (cambiar de reparto a programación web) que solo un modelo no lineal modela con fidelidad.',
        'utilidad': 'Para focalizar subsidios o inspecciones laborales, los formuladores deben emplear modelos de ensamble algorítmico, ya que los modelos paramétricos tradicionales descartan a la mayoría de informales en transición.',
        'limitacion': 'Menor interpretabilidad directa de cada parámetro frente a los coeficientes beta de una regresión logística tradicional.'
    },
    {
        'codigo': 'KO-2.1',
        'seccion': 'Aprendizaje No Supervisado',
        'titulo': 'Segmentación tripartita de vulnerabilidad: El cluster C1 como trampa de subsistencia',
        'resumen': 'El clustering k-Means (k=3) identifica un cluster C1 masivo donde el 72% no cotiza (Chi-cuadrado 553.07, p=0.000), caracterizado por jornadas extremas y baja tarifa horaria.',
        'pregunta': '¿Se forman grupos naturales de trabajadores según sus métricas de jornada e ingreso, sin considerar previamente su estatus de pensión?',
        'variables': 'horas_semanales, ingreso_neto_hora_usd, edad, ingreso_bruto, costos_operativos (estandarizadas)',
        'procedimiento': 'Estandarización Z-score + k-Means (k=3), proyección en Silhouette Plot y contraste bivariado Box Plot con Chi-cuadrado.',
        'evidencia': 'El Box Plot muestra para C1 un 72% de No cotiza frente a C2 (51%) y C3 (50%). La prueba de independencia es contundente: Chi^2 = 553.07 (p < 0.0001 con 2 grados de libertad).',
        'hallazgo': 'El algoritmo agrupa objetivamente a los trabajadores más precarizados en C1, sin haber recibido la etiqueta de pensión durante el entrenamiento. Este grupo combina más de 52 horas semanales con tarifas inferiores a 3 USD/hora.',
        'interpretacion': 'Demuestra que la falta de cotización a pensión no es una conducta negligente del individuo, sino una consecuencia estructural del perfil de explotación horaria en plataformas físicas.',
        'utilidad': 'Permite diseñar políticas segmentadas: en lugar de fiscalizar a todo el universo, focalizar inspección de horas y programas de reconversión laboral específicamente en el Cluster C1.',
        'limitacion': 'k-Means asume clusters esféricos; perfiles fronterizos entre C2 y C3 presentan coeficientes de Silhouette moderados.'
    },
    {
        'codigo': 'KO-2.2',
        'seccion': 'Aprendizaje No Supervisado',
        'titulo': 'Divergencia en el espacio bivariado: Dispersión masiva a baja tarifa',
        'resumen': 'El Scatter Plot revela una aglomeración masiva en tarifas netas bajas (< 2 desviaciones) donde trabajar más horas no mejora la protección social, confirmando la trampa de autoexplotación.',
        'pregunta': '¿Existe correlación visual entre mayor dedicación horaria y mejor probabilidad de afiliación formal?',
        'variables': 'ingreso_neto_hora_usd (X) vs horas_semanales (Y), coloreado por afiliacion_pension',
        'procedimiento': 'Diagrama de dispersión de alta resolución con 12.350 observaciones estandarizadas en Orange3 Scatter Plot.',
        'evidencia': 'Los puntos rojos (No cotiza) se apilan densamente en una columna vertical estrecha en X < 2.0 que recorre todo el eje Y desde -2.5 hasta +2.5 desviaciones de horas. Los azules (Cotiza) se dispersan hacia la derecha en X > 2.0.',
        'hallazgo': 'Dentro del cuadrante de baja remuneración horaria, aumentar las horas no conduce a la formalidad pensional: los trabajadores simplemente agotan su jornada para cubrir costos fijos.',
        'interpretacion': 'Respalda la hipótesis del "trabajador atrapado": en plataformas de entrega o transporte, la tarifa horaria es tan baja que no genera excedente para cotizar, sin importar que se laboren 70 horas a la semana.',
        'utilidad': 'Sustenta la necesidad de un piso tarifario mínimo por hora o por carrera/entrega que incluya el recargo obligatorio para seguridad social.',
        'limitacion': 'Diseño transversal; no registra el paso temporal de un trabajador a lo largo de los meses.'
    },
    {
        'codigo': 'KO-3.1',
        'seccion': 'Minería de Texto (YouTube)',
        'titulo': 'Disonancia temporal en el discurso: Red de liquidez rápida vs ruina pensional a largo plazo',
        'resumen': 'El modelado LDA (7 tópicos, Coherencia 0.408) y el Corpus Viewer descubren que los propios repartidores reconocen que la app sirve para dinero inmediato pero es insostenible en el largo plazo.',
        'pregunta': '¿Qué preocupaciones no estructuradas expresan los trabajadores de plataformas en comunidades digitales abiertas?',
        'variables': '242 comentarios depurados del video OXT8xdqcAoU, vectorizados por Bag of Words TF-IDF y procesados con LDA.',
        'procedimiento': 'Extracción automatizada vía YouTube Data API v3, filtrado de stopwords y cálculo de perplejidad y coherencia temática.',
        'evidencia': 'El comentario con más likes (539) expresa: "freelancing is definitely a good support net for quick money. It\'s safe for part timers, but maybe not in the long run". Coherencia de tópicos: 0.40812.',
        'hallazgo': 'Existe una plena conciencia del trabajador sobre la trampa de corto plazo: las plataformas resuelven la urgencia de efectivo diario, pero transfieren todo el riesgo de invalidez, enfermedad y vejez al individuo.',
        'interpretacion': 'El discurso social no celebra la "libertad" de ser su propio jefe como postula el marketing corporativo; la narrativa dominante es de resignación ante la falta de empleo formal con prestaciones.',
        'utilidad': 'Permite contrarrestar narrativas de lobby empresarial y fundamentar reformas laborales con evidencia cualitativa de primera mano.',
        'limitacion': 'Los comentarios de YouTube provienen de una muestra autoseleccionada que comenta en videos específicos, con posible sesgo hacia quejas o reflexiones críticas.'
    },
    {
        'codigo': 'KO-3.2',
        'seccion': 'Minería de Texto (YouTube)',
        'titulo': 'Saturación léxica en salud y cobertura: Validación empírica del vacío institucional',
        'resumen': 'La nube de palabras destaca términos como health, insurance, benefits y money junto a freelancing, conectando cualitativamente con el hallazgo supervisado de que la salud y ARL determinan la protección.',
        'pregunta': '¿Coinciden los términos más frecuentes en comentarios con las variables más predictivas de los modelos supervisados?',
        'variables': 'Frecuencias de términos tokenizados en Word Cloud y Topic Modelling.',
        'procedimiento': 'Generación de Word Cloud ponderada por TF-IDF y análisis de coocurrencia en Orange Text Mining.',
        'evidencia': 'Términos con alta frecuencia: freelancing (47), work (33), job (29), gig (27), money (17), health (14), insurance (12), pay (12), hours (11). El Tópico 1 asocia directamente gig + economy + health.',
        'hallazgo': 'La salud (health) y el seguro (insurance) aparecen espontáneamente como prioridades en el vocabulario de los usuarios, coincidiendo con el resultado del widget Rank donde cuenta_con_arl y afiliacion_salud lideran la importancia.',
        'interpretacion': 'Triangulación metodológica completa: la variable que matemáticamente mejor predice la cotización en el modelo supervisado es idéntica a la preocupación recurrente que los trabajadores exteriorizan en el plano cualitativo.',
        'utilidad': 'Demuestra solidez científica ante comités evaluadores y reguladores al cerrar la brecha entre modelos cuantitativos y experiencia humana de los trabajadores.',
        'limitacion': 'El análisis de texto en esta muestra incluye comentarios en inglés provenientes de audiencias globales del debate analizado.'
    }
]

def get_etapa6_summary():
    """Retorna el paquete consolidado de datos para las vistas de la Etapa 6."""
    return {
        'metodologia': METODOLOGIA_ORANGE,
        'supervisado': SUPERVISADO_DATA,
        'clustering': CLUSTERING_DATA,
        'texto': TEXT_MINING_DATA,
        'conocimientos': CONOCIMIENTOS_OCULTOS
    }
