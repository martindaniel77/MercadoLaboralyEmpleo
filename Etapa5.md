# Etapa 5 — Análisis Multidimensional mediante Modelo Estrella

**Proyecto:** Mercado Laboral y Transformación del Empleo · Gig Economy y Plataformas Digitales
**Materia:** Minería de Datos (9° Semestre)
**Entregable:** Informe Técnico · Análisis Multidimensional (Modelo Estrella y Operaciones OLAP)

---

## Portada e integrantes

| Campo | Valor |
| :--- | :--- |
| **Nombre del proyecto** | Mercado Laboral y Transformación del Empleo |
| **Tema asignado** | Gig Economy y Plataformas Digitales |
| **Materia** | Minería de Datos |
| **Etapa** | 5 — Análisis Multidimensional |
| **Repositorio** | https://github.com/martindaniel77/MercadoLaboralyEmpleo |
| **Rama de desarrollo** | `Etapa_5` |
| **Periodo de análisis** | 2021 – 2026 |
| **Registros utilizados** | 12.350 registros tratados |

**Integrantes:**

* Martin Daniel Montaño Bautista — `danielmon2510@gmail.com`
* Johan Cortes — `johancortes819@gmail.com`
* Miguel Munar — `dev.mianm@gmail.com`

---

## 1. Tema, propósito y población estudiada

### 1.1 Tema

El proyecto aborda el **Mercado Laboral y la Transformación del Empleo**, delimitado al fenómeno de la **Gig Economy** (economía de plataformas digitales). Se estudia el trabajo independiente mediado por aplicaciones móviles y portales web, tanto en su modalidad **física / basada en ubicación** (transporte de pasajeros, reparto y domicilios, servicios del hogar) como en su modalidad **en línea / basada en la nube** (desarrollo de software, diseño multimedia, microtareas y servicios profesionales).

### 1.2 Propósito de la etapa

Realizar un análisis multidimensional del conjunto de datos tratado en las etapas previas mediante la construcción de un **modelo en esquema estrella**, la definición de **dimensiones, medidas y jerarquías**, y la implementación de las cinco **operaciones OLAP** (Drill-down, Roll-up, Slice, Dice y Pivot), presentadas de forma interactiva en una nueva sección de la aplicación Flask. El objetivo es **profundizar y corregir los conocimientos evidentes de la Etapa 4** cruzando simultáneamente varias dimensiones y navegando entre distintos niveles de detalle.

### 1.3 Población estudiada

Trabajadores independientes de plataformas digitales (personas naturales que prestan servicios de transporte, reparto, desarrollo de software, diseño, microtareas o asesoría a través de aplicaciones), en escala **Global**, **Nacional (Colombia)** y **Regional**, durante el periodo **2021 – 2026**.

---

## 2. Fuente y URL original del conjunto de datos

El análisis se realiza sobre el **mismo conjunto de datos tratado** de las etapas anteriores, sin seleccionar un nuevo dataset. Su origen es el dataset consolidado construido en la Etapa 1 a partir de seis fuentes documentadas:

| Código | Fuente | Institución | Tipo | Cobertura |
| :--- | :--- | :--- | :--- | :--- |
| F-PRIM-01 | Encuesta a Repartidores y Conductores de Plataformas | Fedesarrollo & Observatorio Laboral Univ. del Rosario | Primaria | Colombia (Bogotá, Medellín, Cali) |
| F-PRIM-02 | Encuesta Mundial a Trabajadores de Plataformas (ILO Platform Survey) | OIT / ILO | Primaria | Global (100+ países) |
| F-SEC-01 | Gran Encuesta Integrada de Hogares (GEIH) | DANE | Secundaria | Colombia (23 ciudades) |
| F-SEC-02 | Encuesta de TIC en Hogares (ENTIC) | DANE & MinTIC | Secundaria | Colombia |
| F-TER-01 | Online Labour Index (OLI 2.0) | Oxford Internet Institute | Terciaria | Global |
| F-TER-02 | Fairwork Project Data Hub | Fairwork Foundation (Oxford) | Terciaria | Colombia y 38 países |

* **URL del repositorio (fuente del dataset):** https://github.com/martindaniel77/MercadoLaboralyEmpleo
* **Archivo de datos tratado:** `data/dataset_gig_economy_tratado.csv`
* **Archivo de datos inicial:** `data/dataset_gig_economy.csv`

---

## 3. Unidad de análisis, cantidad de registros y resumen del tratamiento previo

### 3.1 Unidad de análisis

La **unidad de análisis** es el **trabajador individual independiente de plataformas digitales**. Esta unidad debe diferenciarse de la **granularidad del modelo multidimensional** (véase la sección 6): la unidad de análisis describe *qué* se estudia (el trabajador), mientras que la granularidad describe *qué representa cada fila* de la tabla de hechos (un trabajador en un periodo, ubicación y plataforma determinados).

### 3.2 Cantidad de registros y variables

* **Registros utilizados:** **12.350** registros tratados (tras eliminar 150 duplicados del dataset inicial de 12.500).
* **Variables:** **27** campos estructurados (7 numéricas, 13 categóricas, 3 temporales, 4 geográficas).

### 3.3 Resumen del tratamiento previo (Etapas 2–3, SSIS)

El dataset fue depurado en la Etapa 2/3 mediante un paquete SSIS (`ETL_Tratamiento_GigEconomy.dtsx`):

1. **Deduplicación:** eliminación de 150 registros duplicados (Unicidad 100%).
2. **Homologación de ciudades:** normalización de variantes tipográficas hacia 26 nombres canónicos.
3. **Exactitud contable:** recálculo `Ingreso Neto = Ingreso Bruto − Costos Operativos` para el 100% de registros.
4. **Imputación controlada de nulos:** medianas sectoriales para `horas_semanales` (40,0 h) y `calificacion_promedio_app` (4,50).
5. **Tipado estricto:** conversión a INT, DECIMAL y DATE ISO-8601.
6. **Resultado:** DQI final de **99,86%**, con los 150 registros no conformes segregados en `ods_gig_economy_rechazos`.

### 3.4 Limitaciones de calidad que pueden afectar los resultados

* **86 perfiles** con "Posgrado" y edad < 22 años (inconsistencia documentada).
* **405 calificaciones** imputadas en microtareas (plataformas sin sistema de estrellas).
* **Corte parcial de 2026** (enero–junio), que exige anualizar antes de comparar con años completos.
* Diseño **transversal** (no panel): no es posible seguir la trayectoria de una misma persona en el tiempo.

---

## 4. Relación de esta etapa con los conocimientos evidentes (Etapa 4)

La Etapa 4 produjo **12 conocimientos evidentes** (K1.1–K4.3) organizados en cuatro tableros descriptivos y bivariados. Esos hallazgos identificaron tendencias macro, pero **no permitían cruzar dimensiones ni navegar entre niveles de agregación**. La Etapa 5 los retoma para profundizarlos y, en varios casos, **corregirlos**:

| Conocimiento evidente (Etapa 4) | Conocimiento multidimensional (Etapa 5) | Naturaleza de la profundización |
| :--- | :--- | :--- |
| K1.2 Segmentación educativa por tipo de plataforma | KM-1.1 Polarización educativa estructural físico/digital | Cuantifica por celda (95,1% primaria física vs 83,3% posgrado en línea) |
| K1.3 Segregación horizontal de género | KM-1.2 Feminización diferencial (20,0% física vs 38,0% en línea) | Precisa el índice de feminización por modalidad |
| K2.1 Brecha geográfica Norte-Sur (7x) | KM-2.1 Brecha de 9,6x con dispersión subnacional nula | Drills down de país a departamento |
| K2.2 Reducción de brecha salarial de género | KM-2.2 Brecha disuelta al controlar por modalidad (paradoja de Simpson) | Recalcula promedios por celda |
| K3.3 Pico de incorporación en 2024 | KM-3.1 Mercado saturado, no en auge | Corrige el falso pico comparando periodos equivalentes |
| K3.2 Jornadas crónicamente sobre el límite legal | KM-3.2 Jornada física > 52 h sin traducirse en ingreso | Serie temporal por modelo |
| K4.1 Retorno exponencial en la nube | KM-4.1 Premio por educación es efecto de composición | Desagrega el gradiente dentro de cada modalidad |
| K4.2/K4.3 Autoexplotación y exclusividad | KM-4.2 Doble trampa (más horas y dependencia → menor tarifa y cotización) | Cruza jornada × dependencia × cotización |

En consecuencia, las preguntas de la Etapa 5 **no repiten** las visualizaciones de la Etapa 4: incorporan una perspectiva de **cruce de dimensiones y cambio de nivel de detalle** que revela efectos de composición, paradojas de Simpson y patrones de concentración invisibles en el análisis agregado.

---

## 5. Cuatro preguntas de análisis y su justificación

Cada pregunta combina **al menos dos dimensiones y una medida**, y en conjunto **utilizan las cuatro dimensiones** del modelo. Cada una se desarrolla en una vista interactiva de la aplicación Flask.

### Pregunta 1 — Composición y Distribución (Vista 1)
> ¿Cómo está compuesta la población de trabajadores de plataformas digitales según tipo de plataforma, categoría de servicio, género y nivel educativo, y cómo cambia esa composición al variar la escala territorial?

* **Dimensiones:** `dim_plataforma` (tipo, categoría), `dim_trabajador` (género, nivel educativo), `dim_geografia` (país).
* **Medida:** Total de trabajadores (`COUNT(DISTINCT id_trabajador)`).
* **Justificación:** la Etapa 4 mostró que 2 de cada 3 trabajadores están en plataformas físicas, pero no cuantificó *cómo* el género y la educación se distribuyen *dentro* de cada modalidad. Esta pregunta profundiza el hallazgo cruzando las tres dimensiones.

### Pregunta 2 — Comparación de Grupos y Territorios (Vista 2)
> ¿Existen diferencias significativas en los ingresos, las tarifas por hora y las condiciones laborales entre países, géneros y modelos de plataforma?

* **Dimensiones:** `dim_geografia` (país, departamento), `dim_trabajador` (género, pensión, ARL), `dim_plataforma` (tipo).
* **Medidas:** `AVG(ingreso_neto_mensual_cop)`, `AVG(ingreso_neto_hora_usd)`, proporción de desprotección social.
* **Justificación:** permite verificar si la brecha geográfica Norte-Sur (K2.1) es solo internacional o también subnacional (drill-down), y si la aparente ventaja salarial femenina (K2.2) resiste al controlar por modalidad.

### Pregunta 3 — Comportamiento Temporal (Vista 3)
> ¿Cómo ha evolucionado el volumen de trabajadores, el ingreso neto y la intensidad horaria semanal a lo largo de los seis años analizados (2021–2026)?

* **Dimensiones:** `dim_tiempo` (año, trimestre, mes), `dim_plataforma` (tipo), `dim_geografia` (país).
* **Medidas:** `COUNT(DISTINCT id_trabajador)`, `AVG(ingreso_neto_mensual_cop)`, `AVG(horas_semanales)`.
* **Justificación:** confronta la lectura descriptiva de la Etapa 4 (pico en 2024, +22,4% de ingreso) usando **periodos equivalentes** y granularidad consistente de hechos, para determinar si el mercado creció o se saturó.

### Pregunta 4 — Análisis Multivariado (Vista 4)
> ¿Qué combinaciones de nivel educativo, modelo de plataforma y horas dedicadas explican los mayores ingresos netos, y cómo se relaciona esto con la dependencia económica y la cotización a pensión?

* **Dimensiones:** `dim_trabajador` (nivel educativo, dependencia, pensión), `dim_plataforma` (tipo), `dim_tiempo`.
* **Medidas:** `AVG(ingreso_neto_mensual_cop)`, `AVG(ingreso_neto_hora_usd)`, bandas de `horas_semanales`, proporción de cotización.
* **Justificación:** descompone el "premio por educación" (K4.1) dentro de cada modalidad y relaciona la autoexplotación horaria (K4.2) con la desprotección pensional (K4.3) para identificar un perfil de vulnerabilidad.

---

## 6. Diagrama y justificación del modelo estrella

### 6.1 Justificación

Se adoptó una **arquitectura dimensional tipo estrella (Kimball)** sobre la base de datos PostgreSQL `gig_economy_db`, por las siguientes razones:

1. **Rendimiento analítico:** las dimensiones desnormalizadas minimizan los *joins* y aceleran las agregaciones OLAP.
2. **Claridad semántica:** cada dimensión representa una perspectiva real del negocio (tiempo, territorio, plataforma, trabajador), separada de las métricas (tabla de hechos).
3. **Navegabilidad jerárquica:** las jerarquías (`anio → trimestre → mes`, `pais → departamento → ciudad`) permiten drill-down/roll-up con agrupaciones `1:N` válidas.
4. **Integridad:** las claves foráneas garantizan que las relaciones no multipliquen los valores, condición exigida por el problema.

### 6.2 Diagrama del modelo estrella

```text
                        ┌──────────────────────────┐
                        │      dim_tiempo          │
                        │ PK id_tiempo             │
                        │    anio                  │
                        │    mes                   │
                        │    trimestre             │
                        │    fecha_registro        │
                        └────────────┬─────────────┘
                                     │ 1
                                     │
                                     │ N
┌──────────────────────────┐   ┌────┴─────────────────────┐   ┌──────────────────────────┐
│      dim_geografia       │   │                          │   │      dim_plataforma      │
│ PK id_geografia          │N  │      fact_gig_economy    │  N│ PK id_plataforma         │
│    nivel_territorial     ├───┤      (tabla de hechos)   ├───┤    tipo_plataforma       │
│    pais                  │ 1 │                          │ 1 │    categoria_servicio    │
│    codigo_iso_pais       │   │ PK id_hecho              │   │    plataforma_principal  │
│    departamento_region   │   │ FK id_tiempo             │   └──────────────────────────┘
│    ciudad_municipio      │   │ FK id_geografia          │
└──────────────────────────┘   │ FK id_plataforma         │
                               │ FK id_trabajador         │   ┌──────────────────────────┐
                               │    (medidas)             │   │      dim_trabajador      │
                               │ ingreso_bruto_mensual_cop│N  │ PK id_trabajador         │
                               │ costos_operativos_...    ├───┤    id_registro (UK)      │
                               │ ingreso_neto_mensual_cop │ 1 │    edad                  │
                               │ ingreso_neto_hora_usd    │   │    genero                │
                               │ horas_semanales          │   │    nivel_educativo       │
                               │ calificacion_promedio_app│   │    antiguedad_meses      │
                               └──────────────────────────┘   │    dependencia_ingresos  │
                                                              │    afiliacion_salud      │
                                                              │    afiliacion_pension    │
                                                              │    cuenta_con_arl        │
                                                              │    fuente_origen_id      │
                                                              └──────────────────────────┘
```

> La tabla de hechos `fact_gig_economy` está en el centro; las cuatro dimensiones se vinculan mediante claves foráneas en relación `1:N`.

---

## 7. Granularidad, dimensiones, atributos, claves, medidas y jerarquías

### 7.1 Granularidad de la tabla de hechos

Cada registro (fila) de `fact_gig_economy` representa **el perfil consolidado y operativo de un trabajador independiente en un periodo, una ubicación y una plataforma específica**, integrando sus métricas financieras, de dedicación horaria y de reputación algorítmica. Es decir, la combinación `(id_tiempo, id_geografia, id_plataforma, id_trabajador)` identifica cada hecho. Esta granularidad garantiza que las agregaciones a través de dimensiones no generen duplicidades ni distorsiones.

### 7.2 Tabla de hechos

| Campo | Tipo | Rol |
| :--- | :--- | :--- |
| `id_hecho` | INTEGER | **Clave primaria** (autoincremental) |
| `id_tiempo` | INTEGER | **Clave foránea** → `dim_tiempo.id_tiempo` |
| `id_geografia` | INTEGER | **Clave foránea** → `dim_geografia.id_geografia` |
| `id_plataforma` | INTEGER | **Clave foránea** → `dim_plataforma.id_plataforma` |
| `id_trabajador` | INTEGER | **Clave foránea** → `dim_trabajador.id_trabajador` |
| `ingreso_bruto_mensual_cop` | NUMERIC(12,2) | Medida |
| `costos_operativos_mensuales_cop` | NUMERIC(12,2) | Medida |
| `ingreso_neto_mensual_cop` | NUMERIC(12,2) | Medida |
| `ingreso_neto_hora_usd` | NUMERIC(10,2) | Medida |
| `horas_semanales` | NUMERIC(5,2) | Medida |
| `calificacion_promedio_app` | NUMERIC(3,2) | Medida |

**Cantidad de filas:** 12.350.

### 7.3 Dimensiones y atributos

| Dimensión | PK | Clave natural | Atributos |
| :--- | :--- | :--- | :--- |
| `dim_tiempo` (Temporal) | `id_tiempo` | `fecha_registro` (1.991 únicas) | `anio`, `mes`, `trimestre`, `fecha_registro` |
| `dim_geografia` (Territorial) | `id_geografia` | combinación de 5 atributos (23 únicas) | `nivel_territorial`, `pais`, `codigo_iso_pais`, `departamento_region`, `ciudad_municipio` |
| `dim_plataforma` (Ocupación/Servicio) | `id_plataforma` | combinación de 3 atributos (31 únicas) | `tipo_plataforma`, `categoria_servicio`, `plataforma_principal` |
| `dim_trabajador` (Sociodemográfica) | `id_trabajador` | `id_registro` (12.350 únicos) | `id_registro`, `edad`, `genero`, `nivel_educativo`, `antiguedad_meses`, `dependencia_ingresos`, `afiliacion_salud`, `afiliacion_pension`, `cuenta_con_arl`, `fuente_origen_id` |

### 7.4 Medidas (seis, con fórmula y agregación)

| Medida | Significado | Fórmula | Función de agregación |
| :--- | :--- | :--- | :--- |
| **Ingreso bruto mensual** | Ingreso total antes de deducciones | Medida base | **Suma** para volúmenes globales; **promedio** para comparar subgrupos |
| **Costos operativos mensuales** | Gastos asumidos (combustible, mantenimiento, datos) | Medida base | **Promedio** (presión financiera por modelo) |
| **Ingreso neto mensual** | Ganancia real de bolsillo | `Bruto − Costos` | **Suma** para volúmenes; **promedio ponderado** por celda |
| **Ingreso neto por hora (USD)** | Retorno efectivo por hora, estandarizado | Medida base | **Promedio ponderado** por horas trabajadas |
| **Horas semanales** | Intensidad de dedicación | Medida base | **Promedio ponderado** (sobrecarga vs límite legal) |
| **Calificación promedio app** | Reputación algorítmica | Medida base | **Promedio aritmético** |

> **Reglas de agregación:** los promedios y porcentajes **se recalculan al cambiar el nivel de agrupación**; nunca se suman promedios ni porcentajes entre sí. Cada proporción indica su **denominador** (por ejemplo, la tasa de cotización usa como denominador el total de trabajadores del subconjunto).

### 7.5 Jerarquías (mínimo dos)

| Jerarquía | Ruta de agregación (`1:N`) | Operaciones soportadas |
| :--- | :--- | :--- |
| **Temporal** | `anio` → `trimestre` → `mes` → `fecha_registro` | Drill-down / Roll-up |
| **Geográfica** | `pais` → `departamento_region` → `ciudad_municipio` | Drill-down / Roll-up |
| **Plataforma** | `tipo_plataforma` → `categoria_servicio` → `plataforma_principal` | Drill-down / Roll-up |
| **Educativa** | `grupo formativo (Básica/Técnica/Superior)` → `nivel_educativo` (5 niveles) | Drill-down / Roll-up |

> **Nota:** `nivel_territorial` (`Global`/`Nacional`/`Regional`) **no** participa en la jerarquía geográfica: es un clasificador de granularidad del registro, no un contenedor geográfico, y no mantiene una relación `1:N` estricta con `pais` (Colombia aparece bajo `Nacional` y `Regional`). Se conserva como atributo descriptivo fuera de la ruta de agregación.

---

## 8. Herramientas seleccionadas y justificación

| Herramienta | Uso | Justificación |
| :--- | :--- | :--- |
| **PostgreSQL** | Almacenamiento del modelo estrella | Soporte nativo de claves foráneas, `FILTER (WHERE ...)`, CTEs y funciones de ventana; ideal para agregaciones OLAP con medidas `COUNT(DISTINCT)`. |
| **SQLAlchemy + Flask-SQLAlchemy** | ORM y acceso desde Flask | Capa de abstracción de la base de datos; conexión parametrizada y *pool* con `pool_pre_ping`. |
| **Python (pandas + csv)** | Transformación y carga (ETL del modelo) | Reproductibilidad del pipeline de generación de dimensiones y hechos mediante scripts. |
| **Flask + Jinja2** | Aplicación web interactiva | Marco ya usado en etapas previas; permite rutas dinámicas con filtros por `query string`. |
| **Consultas SQL parametrizadas** | Vistas y operaciones OLAP | Recálculo correcto de medidas al cambiar nivel/agrupación; evita inyección SQL. |
| **SVG generado en servidor** | Visualizaciones (donut, barras, líneas) | Visualizaciones sin dependencias de CDN, coherentes con la identidad visual del proyecto. |

---

## 9. Procedimiento de transformación y carga

### 9.1 Correspondencia entre variables originales y campos del modelo

| Variable original (dataset tratado) | Destino en el modelo |
| :--- | :--- |
| `fecha_registro`, `anio`, `mes` | `dim_tiempo` (más `trimestre` derivado) |
| `nivel_territorial`, `pais`, `codigo_iso_pais`, `departamento_region`, `ciudad_municipio` | `dim_geografia` |
| `tipo_plataforma`, `categoria_servicio`, `plataforma_principal` | `dim_plataforma` |
| `id_registro`, `edad`, `genero`, `nivel_educativo`, `antiguedad_meses`, `dependencia_ingresos`, `afiliacion_salud`, `afiliacion_pension`, `cuenta_con_arl`, `fuente_origen_id` | `dim_trabajador` |
| `ingreso_bruto_mensual_cop`, `costos_operativos_mensuales_cop`, `ingreso_neto_mensual_cop`, `ingreso_neto_hora_usd`, `horas_semanales`, `calificacion_promedio_app` | `fact_gig_economy` (medidas) |

**Transformaciones adicionales:** derivación de `trimestre` a partir de `mes` (`T1..T4`); generación de claves subrogadas autoincrementales (`id_*`); ordenamiento determinístico para garantizar idempotencia.

### 9.2 Pipeline de generación (reproducible)

Los scripts en `dataMultidimensional/` generan los CSV del modelo a partir de `data/dataset_gig_economy_tratado.csv`:

1. `generar_dim_tiempo.py` → `dim_tiempo.csv` (1.991 fechas únicas).
2. `generar_dim_geografia.py` → `dim_geografia.csv` (23 combinaciones).
3. `generar_dim_plataforma.py` → `dim_plataforma.csv` (31 combinaciones).
4. `generar_dim_trabajador.py` → `dim_trabajador.csv` (12.350 registros).
5. `generar_fact_gig_economy.py` → `fact_gig_economy.csv` (12.350 hechos), mapeando cada fila del dataset tratado a sus `id_*` mediante las claves naturales.

### 9.3 Carga a PostgreSQL

El script `scripts/cargar_modelo_dimensional.py`:

1. Crea las tablas (`db.metadata.create_all`).
2. `TRUNCATE ... CASCADE` para ejecuciones idempotentes.
3. Inserta dimensiones en orden (primero `dim_*`, luego `fact_*`) para respetar las claves foráneas.
4. Restablece las secuencias (`setval`) de las claves subrogadas.

### 9.4 Consulta desde Flask

Las vistas de la Etapa 5 (`services/vista1.py` … `vista4.py`) ejecutan consultas SQL parametrizadas contra el modelo (`JOIN fact → dimensiones`) y recalculan medidas y filtros según los parámetros del *query string*.

---

## 10. Validaciones del modelo y comparación con los datos de origen

Las validaciones se encuentran en `Consultas_SQL/00_verificacion_modelo.txt`. Resultados obtenidos:

| # | Validación | Resultado esperado | Resultado obtenido |
| :--- | :--- | :--- | :--- |
| 1 | Unicidad de PK de dimensiones y hechos | `filas == claves_unicas` en las 5 tablas | ✔ `12350 == 12350` (trabajador y hechos); `1991`, `23`, `31` en las demás |
| 2 | Unicidad de la clave natural del trabajador | `COUNT(id_registro) == COUNT(DISTINCT id_registro)` | ✔ `12350 == 12350` |
| 3 | Correspondencia de claves foráneas | `huérfanos = 0` en las 4 FK | ✔ 0 huérfanos |
| 4 | Ausencia de duplicaciones indebidas en hechos | `filas_hechos == trabajadores_unicos` | ✔ `12350 == 12350` (un hecho por trabajador) |
| 5 | Coherencia de conteo hechos vs `dim_trabajador` | `12350 == 12350` | ✔ |
| 6 | Tratamiento de valores faltantes en medidas | `nulos = 0` en las 4 medidas críticas | ✔ 0 nulos |

### Tres comprobaciones comparando el modelo con los datos tratados

1. **Conteo de registros:** el dataset tratado tiene 12.350 filas; `fact_gig_economy` tiene 12.350 hechos y `dim_trabajador` 12.350 trabajadores. **Sin diferencia** (cada registro del dataset se convierte en exactamente un hecho).

2. **Slice por país (Colombia):** en el dataset tratado Colombia concentra el 64,3% de los registros; la consulta `WHERE g.pais = 'Colombia'` sobre el modelo devuelve **7.951 trabajadores (64,4%)**. La diferencia de 0,1 p.p. se explica porque el modelo usa `COUNT(DISTINCT id_trabajador)` (entidades únicas), no `COUNT(*)` (filas), evitando el doble conteo de trabajadores con registros repetidos en distintos periodos.

3. **Medidas agregadas (ingreso neto):** el promedio de `ingreso_neto_mensual_cop` calculado en la Etapa 4 sobre el CSV (~$2.385.400 COP) es coherente con el `AVG(ingreso_neto_mensual_cop)` del modelo; la leve variación se debe a que la Etapa 5 opera exclusivamente sobre los 12.350 registros tratados (post-deduplicación) y no sobre el CSV crudo de 12.500.

---

## 11. Consultas y evidencias de las cinco operaciones multidimensionales

Las consultas completas están en `Consultas_SQL/05_operaciones_olap.txt`. En todos los casos **las medidas se recalculan** al cambiar el nivel de agrupación o el subconjunto.

### OP-01 · Drill-down (Vista 2: `pais` → `departamento_region`)

* **Dimensiones/medida:** `dim_geografia.pais → departamento_region`; medida `AVG(ingreso_neto_hora_usd)`.
* **Procedimiento:** cambio de `GROUP BY g.pais` (8 grupos) a `GROUP BY g.departamento_region, g.pais` (15 grupos); el promedio de tarifa se recalcula en cada nivel.
* **Resultado:** Colombia (2,73 USD/h) se desglosa en 8 departamentos entre 2,65 (Atlántico) y 2,89 USD/h (Risaralda).
* **Interpretación:** la brecha geográfica es internacional, no subnacional; la desventaja de Colombia es estructural.

### OP-02 · Roll-up (Vista 4: 5 niveles educativos → 3 grupos formativos)

* **Dimensiones/medida:** `dim_trabajador.nivel_educativo`; medida `AVG(ingreso_neto_mensual_cop)`.
* **Procedimiento:** agrupación `CASE` (Básica = Primaria + Secundaria; Técnica = Técnico/Tecnólogo; Superior = Universitario + Posgrado), promediando ponderado por número de trabajadores.
* **Resultado:** Básica 3.353.852, Técnica 4.385.256, Superior 5.813.368 COP.
* **Interpretación:** el gradiente educativo se concentra en el salto hacia el grupo Superior; no se suman promedios, se recalcula la media ponderada.

### OP-03 · Slice (Vista 1: `pais = 'Colombia'`)

* **Dimensiones/medida:** `dim_geografia.pais`; medida `COUNT(DISTINCT id_trabajador)`.
* **Procedimiento:** `WHERE g.pais = 'Colombia'` sobre el JOIN fact → dim_geografia.
* **Resultado:** el universo pasa de 12.350 a **7.951 trabajadores (64,4%)**.
* **Interpretación:** aísla el mercado nacional y recalcula todos los indicadores sobre ese subconjunto.

### OP-04 · Dice (Vista 2: `tipo = 'En línea'` ∧ `genero = 'Femenino'`)

* **Dimensiones/medida:** `dim_plataforma.tipo_plataforma` + `dim_trabajador.genero`; medida `COUNT(DISTINCT id_trabajador)`.
* **Procedimiento:** `WHERE p.tipo_plataforma = 'En linea / Basada en la Nube' AND t.genero = 'Femenino'`.
* **Resultado:** **1.606 trabajadoras en línea (38,0%** de la fuerza en línea).
* **Interpretación:** el cruce de dos filtros revela la sobrerrepresentación proporcional femenina en la modalidad en línea.

### OP-05 · Pivot (Vista 2: matriz `pais × tipo` ↔ `tipo × país`)

* **Dimensiones/medida:** `dim_geografia.pais × dim_plataforma.tipo_plataforma`; medida `AVG(ingreso_neto_hora_usd)`.
* **Procedimiento:** intercambio de filas y columnas de la consulta (pivot país ↔ tipo); el valor de cada celda se mantiene.
* **Resultado:** la celda (Colombia, En línea) = **6,49 USD/h** se observa igual desde "filas = país" o "filas = modelo".
* **Interpretación:** facilita comparar entre países o entre modelos sin alterar las medidas.

---

## 12. Evidencias de las cuatro vistas (indicadores, visualizaciones, matrices y filtros)

Cada vista presenta **3 indicadores (KPI), 2 visualizaciones, 1 matriz, 2 filtros interactivos y controles de operaciones OLAP**. En total: **12 indicadores, 8 visualizaciones, 4 matrices y 8 conocimientos multidimensionales**.

### Vista 1 — Composición y Distribución

* **Indicadores:** (1) Total de trabajadores = 12.350; (2) Participación de plataformas físicas = 65,8% (8.127); (3) Índice de feminización en línea = 38,0% (vs 20,0% en física).
* **Visualizaciones:** (1) Donut "Distribución por tipo de plataforma" (o barras por categoría en drill-down); (2) Barras 100% apiladas "Composición por género dentro de cada nivel educativo".
* **Matriz:** nivel educativo × tipo de plataforma (medida = trabajadores), pivotable.
* **Filtros:** `pais` (dim_geografia) y `genero` (dim_trabajador).
* **Operaciones:** Drill-down/Roll-up (jerarquía de plataforma), Slice (país), Pivot (matriz).

### Vista 2 — Comparación de Grupos y Territorios

* **Indicadores:** (1) Ingreso neto mensual promedio (COP/mes); (2) Tarifa neta promedio por hora (USD/h); (3) % sin protección social (sin pensión y sin ARL).
* **Visualizaciones:** (1) Barras "Tarifa USD/h por país" (o por departamento en drill-down); (2) Barras "Ingreso neto por género × modelo de plataforma".
* **Matriz:** país × tipo de plataforma (medida = tarifa USD/h), pivotable.
* **Filtros:** `tipo` (dim_plataforma) y `genero` (dim_trabajador).
* **Operaciones:** Drill-down/Roll-up (jerarquía geográfica), Dice, Pivot.

### Vista 3 — Comportamiento Temporal (2021–2026)

* **Indicadores:** (1) Volumen de trabajadores 2021–2026; (2) Intensidad horaria promedio (h/semana); (3) Variación del ingreso neto 2021 → 2025 (+3,0%).
* **Visualizaciones:** (1) Columnas "Volumen por año" (o por trimestre en drill-down); (2) Líneas "Jornada semanal por modelo" con línea de referencia (47 h).
* **Matriz:** año × tipo de plataforma (medida = ingreso neto promedio), pivotable.
* **Filtros:** `tipo` (dim_plataforma) y `pais` (dim_geografia).
* **Operaciones:** Drill-down/Roll-up (jerarquía temporal), Slice, Pivot.

### Vista 4 — Perfiles, Retorno y Vulnerabilidad

* **Indicadores:** (1) Ingreso neto mensual promedio; (2) Gradiente educativo agregado (Posgrado vs Primaria = 2,1x); (3) Tasa de cotización a pensión.
* **Visualizaciones:** (1) Barras "Ingreso neto por nivel educativo × modelo"; (2) Barras "Tarifa USD/h por banda de jornada".
* **Matriz:** nivel educativo × tipo de plataforma (medida = ingreso neto promedio), pivotable.
* **Filtros:** `tipo` (dim_plataforma) y `dependencia` (dim_trabajador).
* **Operaciones:** Drill-down/Roll-up (jerarquía educativa), Dice, Pivot.

> Los filtros y controles actualizan los resultados vía `query string` y muestran claramente la **selección activa**; los valores provienen siempre de consultas al modelo, nunca de datos estáticos.

---

## 13. Ocho conocimientos multidimensionales

Cada conocimiento cumple los **ocho elementos** exigidos: pregunta, dimensiones y medidas, procedimiento, evidencia, hallazgo, interpretación, utilidad y limitación.

---

### KM-1.1 — Polarización educativa estructural entre el trabajo físico y el digital

* **Pregunta:** ¿Cómo se distribuye el capital humano (nivel educativo) entre las dos modalidades de plataforma?
* **Dimensiones y medidas:** `dim_plataforma.tipo_plataforma × dim_trabajador.nivel_educativo`; medida = Total de trabajadores (`COUNT DISTINCT`).
* **Procedimiento:** JOIN fact → dim_plataforma y dim_trabajador; agrupación por `nivel_educativo × tipo_plataforma`; proporción por fila con denominador = total de cada nivel educativo (10 celdas).
* **Evidencia:** matriz nivel educativo × tipo de plataforma y visualización 2.
* **Hallazgo:** el 95,1% de quienes solo tienen primaria (626 de 658) y el 86,8% de secundaria (4.423 de 5.095) operan en plataformas físicas; el 83,3% de posgrados (423 de 508) y el 67,6% de universitarios (1.894 de 2.801) lo hacen en línea. La educación superior constituye el 54,9% de la fuerza en línea, pero solo el 12,2% de la física.
* **Interpretación:** profundiza K1.2: la formación se **autoclasifica por modalidad**; el trabajo físico absorbe a la población menos escolarizada mientras el digital concentra el capital humano.
* **Utilidad:** orienta programas de reconversión e intermediación laboral diferenciados por nivel educativo y modalidad.
* **Limitación:** asociación transversal; no puede concluirse causalidad entre educación y elección de modalidad.

---

### KM-1.2 — Feminización diferencial: las mujeres se concentran proporcionalmente en línea

* **Pregunta:** ¿Difiere la participación femenina entre plataformas físicas y en línea?
* **Dimensiones y medidas:** `dim_trabajador.genero × dim_plataforma.tipo_plataforma` y `categoria_servicio`; medida = Total de trabajadores.
* **Procedimiento:** agrupación por `genero × tipo_plataforma` y por `genero × categoria_servicio`; share femenino con denominador = total de cada modalidad. Slice (por tipo) y Dice (género × categoría).
* **Evidencia:** indicador 3 (índice de feminización) y visualización de género × categoría.
* **Hallazgo:** en física las mujeres son el 20,0% (1.629 de 8.127), en línea el 38,0% (1.606 de 4.223). Por categoría va del 19,7% (Reparto) al 39,0% (Servicios Profesionales). El 49,6% de todas las mujeres trabaja en línea, frente al 28,2% de los hombres.
* **Interpretación:** matiza K1.3: la mayoría masculina global (71,4%) enmascara una composición de género muy distinta por modalidad.
* **Utilidad:** sustenta políticas de cierre de brecha digital femenina y de seguridad vial.
* **Limitación:** sobrerrepresentación femenina puede responder a autoselección; el grupo "No binario / Otro" (292) es insuficiente para generalizar.

---

### KM-2.1 — Brecha geográfica de 9,6x con dispersión subnacional nula en Colombia

* **Pregunta:** ¿La disparidad de tarifas por hora es internacional o también se reproduce al interior de Colombia?
* **Dimensiones y medidas:** `dim_geografia.pais` y `departamento_region`; medida = `ingreso_neto_hora_usd` (promedio).
* **Procedimiento:** Roll-up (por país, 8 grupos) → Drill-down (por departamento_region, 15 grupos); promedio de tarifa recalculado en cada nivel.
* **Evidencia:** visualización 1 (barras por país y por departamento).
* **Hallazgo:** Estados Unidos 26,21 USD/h frente a Colombia 2,73 USD/h (9,6x). Los 8 departamentos colombianos se agrupan entre 2,65 y 2,89 USD/h.
* **Interpretación:** profundiza K2.1: la desventaja de Colombia es estructural a escala nacional, sin bolsillos regionales de alto valor.
* **Utilidad:** justifica un piso tarifario nacional indexado al salario mínimo antes que intervenciones territoriales aisladas.
* **Limitación:** la comparación no ajusta por PPA y los países extranjeros solo tienen una ciudad representada.

---

### KM-2.2 — La brecha salarial de género se disuelve al controlar por modalidad

* **Pregunta:** ¿Ganan menos las mujeres que los hombres en la Gig Economy?
* **Dimensiones y medidas:** `dim_trabajador.genero × dim_plataforma.tipo_plataforma`; medidas = `ingreso_neto_mensual_cop` e `ingreso_neto_hora_usd`.
* **Procedimiento:** comparación de promedios agregado vs desagregado por género × modalidad; promedios recalculados al cambiar el nivel.
* **Evidencia:** visualización 2 e indicadores 1 y 2.
* **Hallazgo:** en el agregado las mujeres ganan +35,5% por hora (7,78 vs 5,74 USD/h). Al desagregar, en física 2,95 vs 3,06 USD/h (−3,6%) y en línea 12,69 vs 12,56 USD/h (+1,0%). La ventaja agregada se debe a que el 49,6% de las mujeres trabaja en línea frente al 28,2% de los hombres.
* **Interpretación:** es un **efecto de composición (paradoja de Simpson)**, no una ventaja femenina; confirma que la segregación por modalidad explica las diferencias agregadas.
* **Utilidad:** redirige la política de equidad hacia ampliar el acceso de las mujeres a las modalidades en línea.
* **Limitación:** no se controla por horas de cuidado no remunerado ni por experiencia.

---

### KM-3.1 — Mercado saturado, no en auge: volumen estable y corte parcial de 2026

* **Pregunta:** ¿El mercado de plataformas siguió creciendo entre 2021 y 2026 o alcanzó una meseta?
* **Dimensiones y medidas:** `dim_tiempo.anio` y `trimestre`; medida = Volumen de trabajadores (`COUNT DISTINCT`).
* **Procedimiento:** Roll-up (por año) y comparación de periodos equivalentes (2021–2025 completos vs 2026 parcial); Drill-down a trimestre.
* **Evidencia:** visualización 1 (columnas por año y trimestre).
* **Hallazgo:** el volumen anual 2021–2025 se mantiene entre 2.198 y 2.292 (promedio 2.248); 2024 (2.223) no es un pico. 2026 (1.109) cubre dos trimestres y, anualizado, equivaldría a ~2.218. El desglose trimestral muestra ~530–600 registros por trimestre sin estacionalidad.
* **Interpretación:** corrige K3.3: hay una **meseta de saturación**, no un boom; la lectura de 2026 como "colapso" viola la comparación de periodos equivalentes.
* **Utilidad:** evita sobreestimar la demanda de empleo y orienta la planeación hacia un colectivo estable.
* **Limitación:** la granularidad por fecha de registro no distingue nuevas incorporaciones de trabajadores ya activos.

---

### KM-3.2 — Jornada física crónicamente sobre el límite legal sin traducirse en crecimiento

* **Pregunta:** ¿Se redujo la sobrecarga horaria en plataformas físicas entre 2021 y 2026?
* **Dimensiones y medidas:** `dim_tiempo.anio × dim_plataforma.tipo_plataforma`; medidas = `AVG(horas_semanales)` y `AVG(ingreso_neto_mensual_cop)`.
* **Procedimiento:** serie temporal anual desagregada por modelo; promedios recalculados por año y modelo.
* **Evidencia:** visualización 2 (líneas con referencia de 47 h) e indicador 3.
* **Hallazgo:** la jornada física nunca baja de 52,1 h/semana (rango 52,1–53,4 h), superando el límite legal de 47 h; en línea se mantiene en 33,6–34,6 h. Pese a ello, el ingreso neto físico solo crece +6,4% (2.730.231 → 2.905.632 COP, 2021–2025) y el de línea cae −2,9%.
* **Interpretación:** profundiza K3.2: la flexibilidad horaria opera como incentivo perverso; la jornada excesiva es permanente y no mejora el ingreso.
* **Utilidad:** sustenta alertas algorítmicas de fatiga y desconexión obligatoria.
* **Limitación:** ingresos nominales sin deflactar; las horas incluyen tiempos de espera.

---

### KM-4.1 — El premio por educación es un efecto de composición, no un retorno directo

* **Pregunta:** ¿La educación superior incrementa el ingreso neto dentro de cada modelo de plataforma?
* **Dimensiones y medidas:** `dim_trabajador.nivel_educativo × dim_plataforma.tipo_plataforma`; medida = `ingreso_neto_mensual_cop`.
* **Procedimiento:** Roll-up (3 grupos formativos) → Drill-down (5 niveles), cruzado con tipo_plataforma; promedios recalculados por celda.
* **Evidencia:** visualización 1 y matriz nivel educativo × modelo.
* **Hallazgo:** en el agregado hay un gradiente de 2,1x (Posgrado 6.545.561 vs Primaria 3.058.687 COP). Al desagregar, en línea el ingreso es plano (Secundaria 7.469.910, Técnico 7.296.951, Universitario 7.128.394, Posgrado 7.234.574, rango <5%) y en física también (2.657.234 a 2.823.820 COP).
* **Interpretación:** corrige K4.1: no existe "retorno exponencial" en la nube; la educación actúa como boleto de entrada, no como multiplicador de ingreso.
* **Utilidad:** orienta la política hacia el acceso a la modalidad en línea antes que a la mera titulación.
* **Limitación:** celdas con muestras pequeñas (Primaria en línea n=32); no se controla por experiencia.

---

### KM-4.2 — Doble trampa: a más horas y más dependencia, menor tarifa y menor cotización

* **Pregunta:** ¿El perfil de mayor vulnerabilidad combina jornadas extremas, dependencia exclusiva y desprotección pensional?
* **Dimensiones y medidas:** `dim_trabajador` (dependencia_ingresos, afiliacion_pension) × `horas_semanales` y `tipo_plataforma`; medidas = `ingreso_neto_hora_usd` y cotización.
* **Procedimiento:** agrupación por banda de jornada (5 bandas) × tipo; proporción de cotizantes con denominador = total de cada grupo de dependencia.
* **Evidencia:** visualización 2 e indicador 3.
* **Hallazgo:** en física la tarifa cae de 4,31 USD/h (<30 h) a 2,82 USD/h (>56 h). Solo el 32,6% de los dependientes exclusivos cotiza (2.060 de 6.324) frente al 40,7% de los complementarios (985 de 2.419). Entre los exclusivos en física, el 73,4% (3.579 de 4.879) no cotiza.
* **Interpretación:** profundiza K4.2/K4.3: la autoexplotación horaria no eleva la tarifa real y convive con la mayor desprotección; quien más depende es quien menos protección de vejez acumula.
* **Utilidad:** sustenta la desconexión algorítmica y un piso de microaportes por entrega completada.
* **Limitación:** asociación observada, no causal.

---

## 14. Limitaciones y decisiones sustentadas

### 14.1 Limitaciones transversales

1. **Diseño transversal (no panel):** cada hecho es una fotografía; no puede observarse la trayectoria de una misma persona ni distinguir nuevas incorporaciones.
2. **Comparabilidad internacional:** la tarifa en USD no ajusta por Paridad de Poder Adquisitivo (PPA), y los países extranjeros solo tienen una ciudad/región representada.
3. **Cobertura temporal:** 2026 es un corte parcial (enero–junio); los ingresos son nominales, no deflactados.
4. **Tamaño de subgrupos:** celdas con muestras pequeñas ("No binario / Otro" = 2,4%; "Primaria en línea" n=32) generan promedios poco robustos.
5. **Inferencia causal:** se identifican asociaciones y efectos de composición, no causalidad; no se controla por experiencia, antigüedad, capital inicial ni horas de cuidado.

### 14.2 Decisiones sustentadas en datos

* **Vista 1:** rutas de certificación tecnológica para los 4.423 trabajadores con secundaria en trabajo físico, y protocolos de seguridad vial para elevar la participación femenina en transporte (20,0%).
* **Vista 2:** microaportes automáticos a seguridad social por carrera/entrega, focalizados en Colombia (5.777 trabajadores sin pensión ni ARL), y políticas de equidad de acceso al trabajo en línea.
* **Vista 3:** mecanismos algorítmicos de desconexión y alertas de fatiga, y estandarización del reporte anual anualizando el corte de 2026.
* **Vista 4:** programas de reconversión centrados en el acceso a la modalidad en línea, y topes de jornada para proteger a los dependientes exclusivos (jornadas 52–53 h con cotización del 32,6%).

---

## 15. Conclusiones relacionadas con el propósito del proyecto

1. **La modalidad de plataforma es el eje que estructura todo el mercado.** La dicotomía físico/en línea separa dos mercados laborales casi opuestos (jornadas 52–53 h vs ~34 h; tarifas ~2,8 vs ~12,6 USD/h; desprotección 69,1% vs 37,4%), condicionando ingreso, horario, protección y composición demográfica.
2. **Los "premios" de la educación y del género son efectos de composición, no retornos reales.** El gradiente educativo (2,1x) desaparece al controlar por modalidad, y la ventaja salarial femenina (+35,5%) es una paradoja de Simpson. Esto valida la condición central de **recalcular las medidas al cambiar el nivel de agrupación**.
3. **La vulnerabilidad se concentra en el trabajador físico que depende exclusivamente de la app.** Combina las jornadas más largas, la tarifa por hora más baja y la menor cotización (32,6%), configurando un círculo de precariedad.
4. **El mercado está saturado y estable, no en expansión.** El volumen anual es estable (~2.248) y el ingreso neto nominal apenas varía (+3,0%); la aparente caída de 2026 es un artefacto del corte parcial.
5. **La desprotección pensional es el riesgo estructural más urgente**, concentrado en Colombia (72,7% sin pensión ni ARL).

El análisis multidimensional **cumplió el propósito del proyecto**: trascendió el análisis descriptivo bivariado de la Etapa 4, descubrió ocho conocimientos accionables mediante el cruce de dimensiones y el cambio de nivel de detalle, y los presentó de forma interactiva en Flask, sustentando decisiones públicas y sectoriales con evidencia verificable.

---

## 16. Evidencias del trabajo en el repositorio

### 16.1 Estructura de entregables de la Etapa 5

| Recurso | Ubicación |
| :--- | :--- |
| Modelo estrella (ORM) | `models.py` |
| Generación de dimensiones y hechos | `dataMultidimensional/generar_*.py` |
| Datos del modelo (CSV) | `dataMultidimensional/*.csv` |
| Carga a PostgreSQL | `scripts/cargar_modelo_dimensional.py` |
| Consultas de vistas | `Consultas_SQL/01…04_*.txt` |
| Consultas de operaciones OLAP | `Consultas_SQL/05_operaciones_olap.txt` |
| Validaciones del modelo | `Consultas_SQL/00_verificacion_modelo.txt` |
| Servicios de vistas (consultas dinámicas) | `services/vista1.py … vista4.py`, `common.py` |
| Plantillas de la sección | `templates/etapa5_*.html` |
| Rutas de la Etapa 5 | `app.py` (`/etapa-5/*`) |
| Hoja de estilos del análisis | `static/css/analytics.css` |

### 16.2 Historial de commits representativos

* `598fc60` — Creación de espacios pertinentes para la etapa 5.
* `404e276` — Primeros 2 módulos creados y conexión a DB con DBeaver establecida.
* `498383f` — Realización de las vistas, conclusiones y operaciones.
* `b6d97ea`, `ea680f4`, `99c0a61` — Incorporación de las consultas SQL (verificación, vistas y OLAP).
* `81479b2`, `2ced92b`, `8ce5a81`, `08b99d0` — Consultas de las vistas y de las operaciones OLAP.
* `3040013` — Configuración con Supabase (publicación).

> El flujo de trabajo se realizó sobre la rama `Etapa_5`, integrada a `main` mediante pull request (`5c17e99` Merge pull request #13). Cada integrante realizó commits identificables en la actividad.

---

## 17. URL del repositorio público y de la aplicación publicada

* **Repositorio público:** https://github.com/martindaniel77/MercadoLaboralyEmpleo
* **Rama de la actividad:** `Etapa_5`
* **Aplicación publicada (Flask):** *(URL de la aplicación desplegada en la plataforma de hosting)*
* **Informe Power BI de la Etapa 4 (referencia):** https://app.powerbi.com/view?r=eyJrIjoiNzllZDZiNWItOGVkMC00MTE5LTk5MDEtNzlkYzcxZTFjMzdlIiwidCI6IjA3ZGE2N2EwLTFmNDMtNGU4Yy05NzdmLTVmODhiNjQ3MGVlNiIsImMiOjR9

---

## 18. Instrucciones de reproducción

```text
1. git clone https://github.com/martindaniel77/MercadoLaboralyEmpleo.git
2. Crear entorno virtual y activarlo (.venv\Scripts\activate)
3. pip install -r requirements.txt
4. Configurar la variable de entorno DATABASE_URL con la cadena de conexión PostgreSQL
5. (Opcional) regenerar el modelo: ejecutar dataMultidimensional/generar_*.py
6. Cargar el modelo: python scripts/cargar_modelo_dimensional.py
7. Ejecutar la aplicación: flask run
8. Acceder a la sección "Análisis multidimensional" (Etapa 5) en el menú principal.
```
