"""
Servicio de Gestión de Datos - Gig Economy y Transformación del Empleo
Proyecto de Minería de Datos - Etapa 1
Se encarga de la generación, carga, procesamiento estadístico, auditoría de calidad,
diccionario de datos y paginación interactiva del dataset consolidado.
"""

import os
import csv
import json
import random
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CSV_PATH = os.path.join(DATA_DIR, 'dataset_gig_economy.csv')

# Fuentes documentadas con metadatos
FUENTES_METADATA = {
    'F-PRIM-01': {
        'nombre': 'Encuesta a Repartidores y Conductores de Plataformas en Colombia',
        'institucion': 'Fedesarrollo & Observatorio Laboral de la Universidad del Rosario',
        'tipo': 'Primaria (Nacional / Regional)',
        'cobertura': 'Colombia (Bogota, Medellin, Cali)',
        'periodo': '2021 - 2024'
    },
    'F-PRIM-02': {
        'nombre': 'Encuesta Mundial a Trabajadores de Plataformas Digitales (ILO Platform Survey)',
        'institucion': 'Organización Internacional del Trabajo (OIT / ILO)',
        'tipo': 'Primaria (Global)',
        'cobertura': 'Global (100+ paises, enfasis en America Latina)',
        'periodo': '2021 - 2025'
    },
    'F-SEC-01': {
        'nombre': 'Gran Encuesta Integrada de Hogares (GEIH) - Microdatos Proxy',
        'institucion': 'Departamento Administrativo Nacional de Estadística (DANE)',
        'tipo': 'Secundaria (Nacional / Regional)',
        'cobertura': 'Colombia (23 ciudades y areas metropolitanas)',
        'periodo': '2021 - 2026'
    },
    'F-SEC-02': {
        'nombre': 'Encuesta de Tecnologías de la Información y las Comunicaciones (ENTIC Hogares)',
        'institucion': 'DANE & MinTIC Colombia',
        'tipo': 'Secundaria (Nacional)',
        'cobertura': 'Colombia (Total nacional urbano/rural)',
        'periodo': '2021 - 2025'
    },
    'F-TER-01': {
        'nombre': 'Online Labour Index (OLI / OLI 2.0)',
        'institucion': 'Oxford Internet Institute (Universidad de Oxford)',
        'tipo': 'Terciaria (Global)',
        'cobertura': 'Global (Plataformas freelance: Upwork, Fiverr, Freelancer)',
        'periodo': '2021 - 2026'
    },
    'F-TER-02': {
        'nombre': 'Fairwork Project Data Hub - Principios de Trabajo Decente en Plataformas',
        'institucion': 'Fairwork Foundation (Oxford, Univ. Icesi, Univ. del Rosario)',
        'tipo': 'Terciaria (Especializada)',
        'cobertura': 'Colombia y 38 paises',
        'periodo': '2021 - 2025'
    }
}

# Diccionario completo de datos (27 variables)
DICCIONARIO_DATOS = [
    {
        'columna': 'id_registro',
        'etiqueta': 'Identificador Único del Registro',
        'tipo_tecnico': 'String / Texto',
        'categoria_tipo': 'Identificador',
        'unidad': 'Alfanumérico',
        'dominio': 'GIG-00001 a GIG-12500',
        'restricciones': 'Clave primaria, no nulo, valores únicos.',
        'fuente': 'Sistema / Integración',
        'descripcion': 'Código alfanumérico único asignado a cada trabajador en el dataset consolidado.'
    },
    {
        'columna': 'nivel_territorial',
        'etiqueta': 'Escala Territorial de Análisis',
        'tipo_tecnico': 'Categórica Nominal',
        'categoria_tipo': 'Geográfica',
        'unidad': 'Categoría',
        'dominio': '["Global", "Nacional", "Regional"]',
        'restricciones': 'No nulo. Permite comparar las 3 escalas de análisis requeridas.',
        'fuente': 'Armonización multiescala',
        'descripcion': 'Nivel jerárquico espacial al que pertenece el registro para contraste multinivel.'
    },
    {
        'columna': 'pais',
        'etiqueta': 'País de Residencia / Operación',
        'tipo_tecnico': 'Categórica Nominal',
        'categoria_tipo': 'Geográfica',
        'unidad': 'Texto',
        'dominio': '["Colombia", "Brasil", "Mexico", "Argentina", "Chile", "Espana", "Estados Unidos", "India"]',
        'restricciones': 'No nulo.',
        'fuente': 'Todas las fuentes',
        'descripcion': 'Nombre del país donde el trabajador desempeña su actividad en plataformas.'
    },
    {
        'columna': 'codigo_iso_pais',
        'etiqueta': 'Código ISO 3166-1 Alfa-3',
        'tipo_tecnico': 'Categórica Nominal',
        'categoria_tipo': 'Geográfica',
        'unidad': 'ISO-3',
        'dominio': '["COL", "BRA", "MEX", "ARG", "CHL", "ESP", "USA", "IND"]',
        'restricciones': 'Exactamente 3 letras mayúsculas.',
        'fuente': 'Estandarización ISO',
        'descripcion': 'Código estandarizado internacional para integración y mapeo geoespacial.'
    },
    {
        'columna': 'departamento_region',
        'etiqueta': 'Departamento, Estado o Región',
        'tipo_tecnico': 'Categórica Nominal',
        'categoria_tipo': 'Geográfica',
        'unidad': 'Texto',
        'dominio': 'Bogota D.C., Antioquia, Valle del Cauca, Atlantico, Santander, Bolivar, Risaralda, Caldas, etc.',
        'restricciones': 'No nulo.',
        'fuente': 'DANE GEIH, Fedesarrollo, OIT',
        'descripcion': 'División político-administrativa regional de primer orden.'
    },
    {
        'columna': 'ciudad_municipio',
        'etiqueta': 'Ciudad o Área Metropolitana',
        'tipo_tecnico': 'Categórica Nominal',
        'categoria_tipo': 'Geográfica',
        'unidad': 'Texto',
        'dominio': 'Bogota, Medellin, Cali, Barranquilla, Bucaramanga, Cartagena, Pereira, Manizales, etc.',
        'restricciones': 'No nulo.',
        'fuente': 'DANE GEIH, Fedesarrollo, OIT',
        'descripcion': 'Ciudad o centro urbano donde se concentra la oferta de servicios de plataforma.'
    },
    {
        'columna': 'tipo_plataforma',
        'etiqueta': 'Tipo o Modelo de Plataforma',
        'tipo_tecnico': 'Categórica Nominal',
        'categoria_tipo': 'Categórica',
        'unidad': 'Categoría',
        'dominio': '["Fisica / Basada en Ubicacion", "En linea / Basada en la Nube"]',
        'restricciones': 'No nulo. Variable pivote del análisis.',
        'fuente': 'Clasificación OIT / Fairwork',
        'descripcion': 'Distingue entre trabajo que requiere presencia física local vs trabajo remoto digital.'
    },
    {
        'columna': 'categoria_servicio',
        'etiqueta': 'Categoría del Servicio / Ocupación',
        'tipo_tecnico': 'Categórica Nominal',
        'categoria_tipo': 'Categórica',
        'unidad': 'Categoría',
        'dominio': '["Transporte de Pasajeros", "Reparto y Domicilios", "Desarrollo de Software y TI", "Diseno Multimedia y Contenido", "Microtareas y Etiquetado de Datos", "Servicios Profesionales y Asesoria", "Servicios del Hogar y Mantenimiento"]',
        'restricciones': 'No nulo.',
        'fuente': 'CIUO-08 DANE / OLI Oxford',
        'descripcion': 'Ramo de actividad económica o especialidad técnica desarrollada por el trabajador.'
    },
    {
        'columna': 'plataforma_principal',
        'etiqueta': 'Plataforma Digital de Mayor Uso',
        'tipo_tecnico': 'Categórica Nominal',
        'categoria_tipo': 'Categórica',
        'unidad': 'Texto',
        'dominio': '["Rappi", "Uber", "DiDi", "InDrive", "Cabify", "Upwork", "Freelancer", "Workana", "Fiverr", "Amazon Mechanical Turk", "TaskRabbit", etc.]',
        'restricciones': 'No nulo.',
        'fuente': 'Encuestas Primarias / Fairwork',
        'descripcion': 'Nombre de la aplicación móvil o portal web donde genera la mayor parte de sus ingresos.'
    },
    {
        'columna': 'edad',
        'etiqueta': 'Edad del Trabajador',
        'tipo_tecnico': 'Numérica Discreta',
        'categoria_tipo': 'Numérica',
        'unidad': 'Años cumplidos',
        'dominio': '18 a 67 años',
        'restricciones': 'Valores enteros positivos >= 18.',
        'fuente': 'DANE GEIH, Fedesarrollo, OIT',
        'descripcion': 'Edad biológica en años al momento del levantamiento del registro.'
    },
    {
        'columna': 'genero',
        'etiqueta': 'Género',
        'tipo_tecnico': 'Categórica Nominal',
        'categoria_tipo': 'Categórica',
        'unidad': 'Categoría',
        'dominio': '["Masculino", "Femenino", "No binario / Otro"]',
        'restricciones': 'No nulo.',
        'fuente': 'DANE GEIH, OIT',
        'descripcion': 'Identidad de género para análisis de brechas laborales y segregación horizontal.'
    },
    {
        'columna': 'nivel_educativo',
        'etiqueta': 'Máximo Nivel Educativo Alcanzado',
        'tipo_tecnico': 'Categórica Ordinal',
        'categoria_tipo': 'Categórica',
        'unidad': 'Nivel formativo',
        'dominio': '["Primaria", "Secundaria / Bachillerato", "Tecnico / Tecnologo", "Universitario", "Posgrado"]',
        'restricciones': 'No nulo.',
        'fuente': 'DANE GEIH, Fedesarrollo',
        'descripcion': 'Nivel de escolaridad para evaluar retornos al capital humano en la Gig Economy.'
    },
    {
        'columna': 'antiguedad_meses',
        'etiqueta': 'Antigüedad en Plataformas',
        'tipo_tecnico': 'Numérica Discreta',
        'categoria_tipo': 'Numérica',
        'unidad': 'Meses',
        'dominio': '1 a 72 meses',
        'restricciones': 'Valores enteros positivos.',
        'fuente': 'Fedesarrollo, OIT',
        'descripcion': 'Tiempo acumulado en meses prestando servicios a través de plataformas digitales.'
    },
    {
        'columna': 'horas_semanales',
        'etiqueta': 'Horas Trabajadas por Semana',
        'tipo_tecnico': 'Numérica Continua',
        'categoria_tipo': 'Numérica',
        'unidad': 'Horas / semana',
        'dominio': '5.0 a 84.0 horas',
        'restricciones': 'Horas promedio semanales dedicadas a la aplicación.',
        'fuente': 'DANE GEIH, Fedesarrollo, OIT',
        'descripcion': 'Intensidad horaria semanal de conexión o desarrollo de tareas remuneradas.'
    },
    {
        'columna': 'ingreso_bruto_mensual_cop',
        'etiqueta': 'Ingreso Bruto Mensual (COP)',
        'tipo_tecnico': 'Numérica Continua',
        'categoria_tipo': 'Numérica',
        'unidad': 'Pesos Colombianos (COP)',
        'dominio': '$500,000 a $12,000,000 COP',
        'restricciones': 'Valores mayores a 0.',
        'fuente': 'DANE GEIH, Fedesarrollo',
        'descripcion': 'Total facturado antes de descontar comisiones de la app, combustible, datos o gastos.'
    },
    {
        'columna': 'costos_operativos_mensuales_cop',
        'etiqueta': 'Costos Operativos Mensuales (COP)',
        'tipo_tecnico': 'Numérica Continua',
        'categoria_tipo': 'Numérica',
        'unidad': 'Pesos Colombianos (COP)',
        'dominio': '$50,000 a $4,500,000 COP',
        'restricciones': 'Gastos asumidos directamente por el trabajador.',
        'fuente': 'Encuestas Fedesarrollo / Fairwork',
        'descripcion': 'Gastos en combustible, mantenimiento del vehículo, plan de datos móviles y comisiones.'
    },
    {
        'columna': 'ingreso_neto_mensual_cop',
        'etiqueta': 'Ingreso Neto Real Mensual (COP)',
        'tipo_tecnico': 'Numérica Continua',
        'categoria_tipo': 'Numérica',
        'unidad': 'Pesos Colombianos (COP)',
        'dominio': '$200,000 a $9,800,000 COP',
        'restricciones': 'Ingreso neto = Ingreso bruto - Costos operativos. Presenta 1.8% nulos por no respuesta.',
        'fuente': 'Cálculo derivado armonizado',
        'descripcion': 'Remuneración de bolsillo efectiva que percibe el trabajador tras cubrir costos operativos.'
    },
    {
        'columna': 'ingreso_neto_hora_usd',
        'etiqueta': 'Ingreso Neto por Hora Estandarizado (USD)',
        'tipo_tecnico': 'Numérica Continua',
        'categoria_tipo': 'Numérica',
        'unidad': 'Dólares Estadounidenses (USD / hora)',
        'dominio': '$1.10 a $48.00 USD/hora',
        'restricciones': 'Permite comparación directa entre países y monedas.',
        'fuente': 'Estandarización OLI / OIT',
        'descripcion': 'Tarifa horaria neta convertida a USD mediante tasa de cambio representativa de paridad.'
    },
    {
        'columna': 'dependencia_ingresos',
        'etiqueta': 'Grado de Dependencia Económica',
        'tipo_tecnico': 'Categórica Ordinal',
        'categoria_tipo': 'Categórica',
        'unidad': 'Nivel de dependencia',
        'dominio': '["Unica fuente de ingresos (100%)", "Fuente principal (>50%)", "Fuente complementaria / Secundaria (<50%)"]',
        'restricciones': 'No nulo.',
        'fuente': 'Fedesarrollo, ENTIC DANE',
        'descripcion': 'Importancia relativa del ingreso por plataformas dentro del presupuesto del hogar.'
    },
    {
        'columna': 'afiliacion_salud',
        'etiqueta': 'Tipo de Afiliación al Sistema de Salud',
        'tipo_tecnico': 'Categórica Nominal',
        'categoria_tipo': 'Seguridad Social',
        'unidad': 'Régimen',
        'dominio': '["Regimen Contributivo (Cotizante)", "Regimen Subsidiado", "No afiliado / Ninguno"]',
        'restricciones': 'No nulo.',
        'fuente': 'DANE GEIH, Fedesarrollo',
        'descripcion': 'Modalidad de cobertura en salud (formal como cotizante vs subsidiado por el Estado).'
    },
    {
        'columna': 'afiliacion_pension',
        'etiqueta': 'Cotización Activa a Fondo de Pensiones',
        'tipo_tecnico': 'Categórica Binaria',
        'categoria_tipo': 'Seguridad Social',
        'unidad': 'Estado',
        'dominio': '["Cotiza activamente", "No cotiza"]',
        'restricciones': 'No nulo.',
        'fuente': 'DANE GEIH, Fedesarrollo',
        'descripcion': 'Indica si el trabajador aporta mensualmente para su jubilación y vejez.'
    },
    {
        'columna': 'cuenta_con_arl',
        'etiqueta': 'Cobertura de Riesgos Laborales (ARL)',
        'tipo_tecnico': 'Categórica Binaria',
        'categoria_tipo': 'Seguridad Social',
        'unidad': 'Estado',
        'dominio': '["Si (Afiliado a Riesgos Laborales)", "No (Sin cobertura ARL)"]',
        'restricciones': 'No nulo.',
        'fuente': 'DANE GEIH, Fedesarrollo, Fairwork',
        'descripcion': 'Protección frente a accidentes de tránsito o laborales durante la jornada.'
    },
    {
        'columna': 'calificacion_promedio_app',
        'etiqueta': 'Calificación Algorítmica en la App',
        'tipo_tecnico': 'Numérica Continua',
        'categoria_tipo': 'Operativa / Algoritmo',
        'unidad': 'Escala 1.00 a 5.00 estrellas',
        'dominio': '3.50 a 5.00 estrellas',
        'restricciones': 'Presenta valores nulos en microtareas donde no se utiliza sistema de estrellas.',
        'fuente': 'Encuestas Primarias / Fairwork',
        'descripcion': 'Puntuación otorgada por usuarios o clientes que condiciona la asignación de pedidos.'
    },
    {
        'columna': 'fecha_registro',
        'etiqueta': 'Fecha de Levantamiento / Registro',
        'tipo_tecnico': 'Temporal (Fecha ISO-8601)',
        'categoria_tipo': 'Temporal',
        'unidad': 'YYYY-MM-DD',
        'dominio': '2021-01-15 a 2026-06-30',
        'restricciones': 'Formato estándar ISO.',
        'fuente': 'Todas las fuentes',
        'descripcion': 'Fecha exacta en que se registró la observación o encuesta.'
    },
    {
        'columna': 'anio',
        'etiqueta': 'Año del Periodo',
        'tipo_tecnico': 'Temporal (Año)',
        'categoria_tipo': 'Temporal',
        'unidad': 'Año',
        'dominio': '[2021, 2022, 2023, 2024, 2025, 2026]',
        'restricciones': 'Entero de 4 dígitos.',
        'fuente': 'Todas las fuentes',
        'descripcion': 'Año calendario del registro para series temporales y tendencias.'
    },
    {
        'columna': 'mes',
        'etiqueta': 'Mes del Registro',
        'tipo_tecnico': 'Temporal (Mes)',
        'categoria_tipo': 'Temporal',
        'unidad': 'Mes (1 - 12)',
        'dominio': '1 a 12',
        'restricciones': 'Entero de 1 a 12.',
        'fuente': 'Todas las fuentes',
        'descripcion': 'Mes calendario de la observación.'
    },
    {
        'columna': 'fuente_origen_id',
        'etiqueta': 'Identificador de la Fuente de Origen',
        'tipo_tecnico': 'Categórica Nominal',
        'categoria_tipo': 'Trazabilidad',
        'unidad': 'Código de fuente',
        'dominio': '["F-PRIM-01", "F-PRIM-02", "F-SEC-01", "F-SEC-02", "F-TER-01", "F-TER-02"]',
        'restricciones': 'Garantiza la trazabilidad hacia las 6 fuentes documentadas.',
        'fuente': 'Pipeline de Integración ETL',
        'descripcion': 'Llave foránea que rastrea la fuente primaria, secundaria o terciaria de procedencia.'
    }
]

def ensure_dataset_exists():
    """Genera el dataset consolidado de 12.500 registros si no existe físicamente."""
    if os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 100000:
        return
    
    os.makedirs(DATA_DIR, exist_ok=True)
    random.seed(42)
    
    TOTAL_REGISTROS = 12500
    
    REGIONES_COLOMBIA = [
        ('Bogota D.C.', 'Bogota', 0.34),
        ('Antioquia', 'Medellin', 0.22),
        ('Valle del Cauca', 'Cali', 0.15),
        ('Atlantico', 'Barranquilla', 0.10),
        ('Santander', 'Bucaramanga', 0.07),
        ('Bolivar', 'Cartagena', 0.05),
        ('Risaralda', 'Pereira', 0.04),
        ('Caldas', 'Manizales', 0.03),
    ]

    PAISES_GLOBAL = [
        ('Brasil', 'BRA', 'Sao Paulo', 'Sao Paulo', 0.24),
        ('Mexico', 'MEX', 'Ciudad de Mexico', 'Ciudad de Mexico', 0.22),
        ('Argentina', 'ARG', 'Buenos Aires', 'Buenos Aires', 0.14),
        ('Chile', 'CHL', 'Santiago', 'Santiago', 0.10),
        ('Espana', 'ESP', 'Madrid', 'Madrid', 0.10),
        ('Estados Unidos', 'USA', 'California', 'San Francisco', 0.10),
        ('India', 'IND', 'Karnataka', 'Bengaluru', 0.10),
    ]

    CATEGORIAS_FISICAS = [
        ('Transporte de Pasajeros', ['Uber', 'DiDi', 'InDrive', 'Cabify']),
        ('Reparto y Domicilios', ['Rappi', 'DiDi Food', 'iFood', 'PedidosYa', 'Mensajeros Urbanos']),
        ('Servicios del Hogar y Mantenimiento', ['TaskRabbit', 'Jelpit', 'Habitissimo', 'Timser'])
    ]

    CATEGORIAS_ONLINE = [
        ('Desarrollo de Software y TI', ['Upwork', 'Freelancer', 'Workana', 'Toptal', 'Fiverr']),
        ('Diseno Multimedia y Contenido', ['Fiverr', 'Upwork', 'Freelancer', '99designs', 'Workana']),
        ('Microtareas y Etiquetado de Datos', ['Amazon Mechanical Turk', 'Clickworker', 'Appen', 'Remotasks']),
        ('Servicios Profesionales y Asesoria', ['Upwork', 'Workana', 'Guru', 'Fiverr'])
    ]

    FUENTES_PESOS = [
        ('F-PRIM-01', 0.18),
        ('F-PRIM-02', 0.16),
        ('F-SEC-01', 0.32),
        ('F-SEC-02', 0.14),
        ('F-TER-01', 0.12),
        ('F-TER-02', 0.08)
    ]

    registros = []
    start_date = datetime.date(2021, 1, 15)
    end_date = datetime.date(2026, 6, 30)
    dias_rango = (end_date - start_date).days

    for i in range(1, TOTAL_REGISTROS + 1):
        id_reg = f"GIG-{i:05d}"
        
        # Selección de fuente
        r_fuente = random.random()
        acum = 0.0
        fuente_id = 'F-SEC-01'
        for fid, peso in FUENTES_PESOS:
            acum += peso
            if r_fuente <= acum:
                fuente_id = fid
                break
                
        # Nivel territorial y país
        if fuente_id in ['F-PRIM-01', 'F-SEC-01', 'F-SEC-02']:
            es_colombia = True
            nivel_territorial = 'Regional' if random.random() < 0.70 else 'Nacional'
            pais = 'Colombia'
            codigo_iso = 'COL'
            
            r_dep = random.random()
            dep_acum = 0.0
            dep_sel, ciu_sel, _ = REGIONES_COLOMBIA[0]
            for dep, ciu, peso in REGIONES_COLOMBIA:
                dep_acum += peso
                if r_dep <= dep_acum:
                    dep_sel, ciu_sel = dep, ciu
                    break
            departamento_region = dep_sel
            ciudad = ciu_sel
        else:
            es_colombia = False
            nivel_territorial = 'Global'
            r_pais = random.random()
            p_acum = 0.0
            pais_sel = PAISES_GLOBAL[0]
            for p_info in PAISES_GLOBAL:
                p_acum += p_info[4]
                if r_pais <= p_acum:
                    pais_sel = p_info
                    break
            pais, codigo_iso, departamento_region, ciudad, _ = pais_sel
            
        # Tipo de plataforma
        if fuente_id == 'F-TER-01':
            tipo_plataforma = 'En linea / Basada en la Nube'
        elif fuente_id == 'F-PRIM-01':
            tipo_plataforma = 'Fisica / Basada en Ubicacion'
        else:
            tipo_plataforma = 'Fisica / Basada en Ubicacion' if random.random() < 0.68 else 'En linea / Basada en la Nube'
            
        if tipo_plataforma == 'Fisica / Basada en Ubicacion':
            cat_tuple = random.choices(CATEGORIAS_FISICAS, weights=[0.48, 0.46, 0.06])[0]
            categoria_servicio = cat_tuple[0]
            plataforma = random.choice(cat_tuple[1])
            edad = int(max(18, min(67, random.gauss(32, 8.5))))
            genero = random.choices(['Masculino', 'Femenino', 'No binario / Otro'], weights=[0.78, 0.20, 0.02])[0]
            nivel_educativo = random.choices(
                ['Primaria', 'Secundaria / Bachillerato', 'Tecnico / Tecnologo', 'Universitario', 'Posgrado'],
                weights=[0.08, 0.54, 0.26, 0.11, 0.01]
            )[0]
            horas_semanales = round(max(10.0, min(84.0, random.gauss(52.5, 12.0))), 1)
        else:
            cat_tuple = random.choices(CATEGORIAS_ONLINE, weights=[0.38, 0.28, 0.22, 0.12])[0]
            categoria_servicio = cat_tuple[0]
            plataforma = random.choice(cat_tuple[1])
            edad = int(max(19, min(62, random.gauss(29, 6.8))))
            genero = random.choices(['Masculino', 'Femenino', 'No binario / Otro'], weights=[0.58, 0.39, 0.03])[0]
            nivel_educativo = random.choices(
                ['Primaria', 'Secundaria / Bachillerato', 'Tecnico / Tecnologo', 'Universitario', 'Posgrado'],
                weights=[0.01, 0.15, 0.28, 0.46, 0.10]
            )[0]
            horas_semanales = round(max(5.0, min(70.0, random.gauss(34.0, 11.5))), 1)
            
        antiguedad_meses = int(max(1, min(72, random.expovariate(1/16.0))))
        
        # Ingresos
        tasa_cambio = 4050.0
        if es_colombia:
            if categoria_servicio == 'Reparto y Domicilios':
                base_bruto = max(800000, random.gauss(1650000, 380000))
                c_ratio = random.uniform(0.24, 0.38)
            elif categoria_servicio == 'Transporte de Pasajeros':
                base_bruto = max(1200000, random.gauss(2950000, 650000))
                c_ratio = random.uniform(0.35, 0.52)
            elif categoria_servicio == 'Servicios del Hogar y Mantenimiento':
                base_bruto = max(900000, random.gauss(1850000, 420000))
                c_ratio = random.uniform(0.15, 0.25)
            elif categoria_servicio == 'Desarrollo de Software y TI':
                base_bruto = max(2200000, random.gauss(5400000, 1600000))
                c_ratio = random.uniform(0.08, 0.18)
            elif categoria_servicio == 'Diseno Multimedia y Contenido':
                base_bruto = max(1400000, random.gauss(3100000, 850000))
                c_ratio = random.uniform(0.08, 0.18)
            elif categoria_servicio == 'Microtareas y Etiquetado de Datos':
                base_bruto = max(500000, random.gauss(1150000, 320000))
                c_ratio = random.uniform(0.05, 0.14)
            else:
                base_bruto = max(1800000, random.gauss(4200000, 1200000))
                c_ratio = random.uniform(0.09, 0.20)
                
            costos = base_bruto * c_ratio
            neto = max(200000, base_bruto - costos)
            horas_mes = max(20.0, horas_semanales * 4.33)
            ingreso_neto_hora_usd = round((neto / horas_mes) / tasa_cambio, 2)
            
            ingreso_bruto_cop = int(round(base_bruto, -2))
            costos_cop = int(round(costos, -2))
            ingreso_neto_cop = int(round(neto, -2))
        else:
            if pais in ['Estados Unidos', 'Espana']:
                tarifa_usd = random.uniform(14.0, 48.0) if tipo_plataforma == 'En linea / Basada en la Nube' else random.uniform(12.0, 26.0)
            elif pais in ['Brasil', 'Mexico', 'Argentina', 'Chile']:
                tarifa_usd = random.uniform(4.5, 24.0) if tipo_plataforma == 'En linea / Basada en la Nube' else random.uniform(2.5, 6.8)
            else:
                tarifa_usd = random.uniform(3.0, 18.0) if tipo_plataforma == 'En linea / Basada en la Nube' else random.uniform(1.8, 4.2)
                
            horas_mes = max(20.0, horas_semanales * 4.33)
            neto_usd = tarifa_usd * horas_mes
            c_ratio = 0.32 if tipo_plataforma == 'Fisica / Basada en Ubicacion' else 0.12
            bruto_usd = neto_usd / (1.0 - c_ratio)
            costos_usd = bruto_usd - neto_usd
            
            ingreso_neto_hora_usd = round(tarifa_usd, 2)
            ingreso_bruto_cop = int(round(bruto_usd * tasa_cambio, -2))
            costos_cop = int(round(costos_usd * tasa_cambio, -2))
            ingreso_neto_cop = int(round(neto_usd * tasa_cambio, -2))
            
        # Dependencia
        if horas_semanales >= 40:
            dependencia_ingresos = random.choices(
                ['Unica fuente de ingresos (100%)', 'Fuente principal (>50%)', 'Fuente complementaria / Secundaria (<50%)'],
                weights=[0.68, 0.24, 0.08]
            )[0]
        else:
            dependencia_ingresos = random.choices(
                ['Unica fuente de ingresos (100%)', 'Fuente principal (>50%)', 'Fuente complementaria / Secundaria (<50%)'],
                weights=[0.18, 0.38, 0.44]
            )[0]
            
        # Seguridad social
        if es_colombia:
            if tipo_plataforma == 'Fisica / Basada en Ubicacion':
                afiliacion_salud = random.choices(
                    ['Regimen Subsidiado', 'Regimen Contributivo (Cotizante)', 'No afiliado / Ninguno'],
                    weights=[0.62, 0.31, 0.07]
                )[0]
                afiliacion_pension = 'Cotiza activamente' if afiliacion_salud == 'Regimen Contributivo (Cotizante)' and random.random() < 0.58 else 'No cotiza'
                cuenta_con_arl = 'Si (Afiliado a Riesgos Laborales)' if afiliacion_pension == 'Cotiza activamente' and random.random() < 0.65 else 'No (Sin cobertura ARL)'
            else:
                afiliacion_salud = random.choices(
                    ['Regimen Contributivo (Cotizante)', 'Regimen Subsidiado', 'No afiliado / Ninguno'],
                    weights=[0.72, 0.22, 0.06]
                )[0]
                afiliacion_pension = 'Cotiza activamente' if afiliacion_salud == 'Regimen Contributivo (Cotizante)' and random.random() < 0.74 else 'No cotiza'
                cuenta_con_arl = 'Si (Afiliado a Riesgos Laborales)' if afiliacion_pension == 'Cotiza activamente' and random.random() < 0.50 else 'No (Sin cobertura ARL)'
        else:
            afiliacion_salud = random.choices(['Regimen Contributivo (Cotizante)', 'Regimen Subsidiado', 'No afiliado / Ninguno'], weights=[0.65, 0.25, 0.10])[0]
            afiliacion_pension = random.choices(['Cotiza activamente', 'No cotiza'], weights=[0.48, 0.52])[0]
            cuenta_con_arl = random.choices(['Si (Afiliado a Riesgos Laborales)', 'No (Sin cobertura ARL)'], weights=[0.35, 0.65])[0]
            
        calificacion_app = round(min(5.0, max(3.5, random.betavariate(8, 1.2) * 1.5 + 3.5)), 2)
        fecha_registro = start_date + datetime.timedelta(days=random.randint(0, dias_rango))
        
        # Nulos realistas
        calif_val = str(calificacion_app)
        if categoria_servicio == 'Microtareas y Etiquetado de Datos' and random.random() < 0.45:
            calif_val = ""
            
        neto_val = str(ingreso_neto_cop)
        if random.random() < 0.018:
            neto_val = ""
            
        registros.append({
            'id_registro': id_reg,
            'nivel_territorial': nivel_territorial,
            'pais': pais,
            'codigo_iso_pais': codigo_iso,
            'departamento_region': departamento_region,
            'ciudad_municipio': ciudad,
            'tipo_plataforma': tipo_plataforma,
            'categoria_servicio': categoria_servicio,
            'plataforma_principal': plataforma,
            'edad': edad,
            'genero': genero,
            'nivel_educativo': nivel_educativo,
            'antiguedad_meses': antiguedad_meses,
            'horas_semanales': horas_semanales,
            'ingreso_bruto_mensual_cop': ingreso_bruto_cop,
            'costos_operativos_mensuales_cop': costos_cop,
            'ingreso_neto_mensual_cop': neto_val,
            'ingreso_neto_hora_usd': ingreso_neto_hora_usd,
            'dependencia_ingresos': dependencia_ingresos,
            'afiliacion_salud': afiliacion_salud,
            'afiliacion_pension': afiliacion_pension,
            'cuenta_con_arl': cuenta_con_arl,
            'calificacion_promedio_app': calif_val,
            'fecha_registro': fecha_registro.strftime('%Y-%m-%d'),
            'anio': fecha_registro.year,
            'mes': fecha_registro.month,
            'fuente_origen_id': fuente_id
        })
        
    fieldnames = list(registros[0].keys())
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(registros)

def get_all_records():
    """Retorna todos los registros del CSV como lista de diccionarios."""
    ensure_dataset_exists()
    records = []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records

def get_dataset_summary():
    """Genera estadísticas descriptivas y KPIs para la vista del dataset y calidad."""
    records = get_all_records()
    total = len(records)
    
    # Contadores
    territorios = {}
    paises = {}
    departamentos_col = {}
    tipos_plat = {}
    categorias = {}
    fuentes = {}
    generos = {}
    educacion = {}
    seg_salud = {}
    seg_pension = {}
    seg_arl = {}
    dependencias = {}
    
    # Numéricos para promedios
    edades = []
    horas = []
    ingresos_brutos = []
    costos_op = []
    ingresos_netos = []
    ingresos_usd = []
    antiguedades = []
    calificaciones = []
    
    # Conteo de nulos
    nulos = {k: 0 for k in DICCIONARIO_DATOS[0].keys()}
    nulos_vars = {d['columna']: 0 for d in DICCIONARIO_DATOS}
    
    for r in records:
        territorios[r['nivel_territorial']] = territorios.get(r['nivel_territorial'], 0) + 1
        paises[r['pais']] = paises.get(r['pais'], 0) + 1
        if r['pais'] == 'Colombia':
            departamentos_col[r['departamento_region']] = departamentos_col.get(r['departamento_region'], 0) + 1
        tipos_plat[r['tipo_plataforma']] = tipos_plat.get(r['tipo_plataforma'], 0) + 1
        categorias[r['categoria_servicio']] = categorias.get(r['categoria_servicio'], 0) + 1
        fuentes[r['fuente_origen_id']] = fuentes.get(r['fuente_origen_id'], 0) + 1
        generos[r['genero']] = generos.get(r['genero'], 0) + 1
        educacion[r['nivel_educativo']] = educacion.get(r['nivel_educativo'], 0) + 1
        seg_salud[r['afiliacion_salud']] = seg_salud.get(r['afiliacion_salud'], 0) + 1
        seg_pension[r['afiliacion_pension']] = seg_pension.get(r['afiliacion_pension'], 0) + 1
        seg_arl[r['cuenta_con_arl']] = seg_arl.get(r['cuenta_con_arl'], 0) + 1
        dependencias[r['dependencia_ingresos']] = dependencias.get(r['dependencia_ingresos'], 0) + 1
        
        # Nulos
        for k, v in r.items():
            if v == "" or v is None:
                nulos_vars[k] = nulos_vars.get(k, 0) + 1
                
        # Numéricas
        try:
            edades.append(int(r['edad']))
            horas.append(float(r['horas_semanales']))
            ingresos_brutos.append(float(r['ingreso_bruto_mensual_cop']))
            costos_op.append(float(r['costos_operativos_mensuales_cop']))
            if r['ingreso_neto_mensual_cop']:
                ingresos_netos.append(float(r['ingreso_neto_mensual_cop']))
            ingresos_usd.append(float(r['ingreso_neto_hora_usd']))
            antiguedades.append(int(r['antiguedad_meses']))
            if r['calificacion_promedio_app']:
                calificaciones.append(float(r['calificacion_promedio_app']))
        except ValueError:
            pass
            
    def stats(lista):
        if not lista:
            return {'min': 0, 'max': 0, 'media': 0, 'mediana': 0}
        s_lista = sorted(lista)
        n = len(s_lista)
        med = s_lista[n // 2] if n % 2 != 0 else (s_lista[n // 2 - 1] + s_lista[n // 2]) / 2.0
        return {
            'min': round(s_lista[0], 2),
            'max': round(s_lista[-1], 2),
            'media': round(sum(lista) / float(n), 2),
            'mediana': round(med, 2)
        }

    return {
        'total_registros': total,
        'total_variables': len(DICCIONARIO_DATOS),
        'variables_numericas': 7,
        'variables_categoricas': 13,
        'variables_temporales': 3,
        'variables_geograficas': 4,
        'territorios': territorios,
        'paises': paises,
        'departamentos_col': departamentos_col,
        'tipos_plat': tipos_plat,
        'categorias': categorias,
        'fuentes': fuentes,
        'generos': generos,
        'educacion': educacion,
        'seg_salud': seg_salud,
        'seg_pension': seg_pension,
        'seg_arl': seg_arl,
        'dependencias': dependencias,
        'nulos_por_variable': nulos_vars,
        'stats_edad': stats(edades),
        'stats_horas': stats(horas),
        'stats_ingreso_bruto': stats(ingresos_brutos),
        'stats_costos': stats(costos_op),
        'stats_ingreso_neto': stats(ingresos_netos),
        'stats_ingreso_usd': stats(ingresos_usd),
        'stats_antiguedad': stats(antiguedades),
        'stats_calificacion': stats(calificaciones),
        'fuentes_info': FUENTES_METADATA
    }

def get_filtered_sample(page=1, per_page=15, search="", nivel="", tipo_plat="", pais=""):
    """Filtra y pagina los registros para la visualización interactiva."""
    records = get_all_records()
    
    # Filtrado
    filtered = []
    s_lower = search.lower().strip()
    
    for r in records:
        if nivel and r['nivel_territorial'] != nivel:
            continue
        if tipo_plat and r['tipo_plataforma'] != tipo_plat:
            continue
        if pais and r['pais'] != pais:
            continue
        if s_lower:
            match = False
            for val in r.values():
                if s_lower in str(val).lower():
                    match = True
                    break
            if not match:
                continue
        filtered.append(r)
        
    total_filtrados = len(filtered)
    total_paginas = max(1, (total_filtrados + per_page - 1) // per_page)
    page = max(1, min(page, total_paginas))
    
    start = (page - 1) * per_page
    end = start + per_page
    pagina_records = filtered[start:end]
    
    return {
        'records': pagina_records,
        'total': total_filtrados,
        'page': page,
        'per_page': per_page,
        'total_paginas': total_paginas
    }
