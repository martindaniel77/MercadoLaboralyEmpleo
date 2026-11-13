# Etapa 6 — Aprendizaje Automático y Conocimiento Oculto en Orange Data Mining

**Proyecto:** Mercado Laboral y Transformación del Empleo · Gig Economy y Plataformas Digitales  
**Materia:** Minería de Datos (9° Semestre)  
**Entregable:** Informe Técnico · Modelos Supervisados, Clustering No Supervisado y Minería de Texto en Orange3  

---

## Portada e Integrantes

| Campo | Valor |
| :--- | :--- |
| **Nombre del proyecto** | Mercado Laboral y Transformación del Empleo |
| **Tema asignado** | Gig Economy y Plataformas Digitales |
| **Materia** | Minería de Datos |
| **Etapa** | 6 — Conocimiento Oculto (Orange Data Mining) |
| **Software empleado** | Orange Data Mining v3.40.0 (x86_64) + Add-on Orange3-Text |
| **Repositorio** | https://github.com/martindaniel77/MercadoLaboralyEmpleo |
| **Archivo de flujo Orange** | `Orange3_GIG/GIG ECONOMY.ows` |
| **Registros cuantitativos** | 12.350 registros tratados (`data/dataset_gig_economy_tratado.csv`) |
| **Corpus de texto** | 242 comentarios de YouTube depurados (Video ID: `OXT8xdqcAoU`) |

**Integrantes:**
* Martin Daniel Montaño Bautista — `danielmon2510@gmail.com`
* Johan Cortes — `johancortes819@gmail.com`
* Miguel Munar — `dev.mianm@gmail.com`

---

## 1. Propósito de la Etapa y Pregunta de Investigación

El propósito de la **Etapa 6** es superar el análisis descriptivo y multidimensional previo mediante técnicas avanzadas de **Minería de Datos y Machine Learning en Orange Data Mining**, descubriendo patrones no lineales, reglas inductivas, agrupamientos naturales y percepciones cualitativas que permanecían ocultos en los datos:

1. **Aprendizaje Supervisado:** Predecir la probabilidad de que un trabajador cotice a pensión e identificar los factores condicionantes primarios de la protección social formal.
2. **Aprendizaje No Supervisado:** Agrupar naturalmente a los trabajadores en clusters de vulnerabilidad según variables objetivas de jornada, ingresos y costos, sin intervención de la variable de pensión.
3. **Minería de Texto:** Extraer y modelar probabilísticamente temas latentes en comentarios públicos de YouTube para contrastar el discurso social vivo con la evidencia matemática.

---

## 2. Sección 1 · Modelos Supervisados y Predicción de Cotización

### 2.1 Formulación del Problema
* **Tipo de problema:** Clasificación Binaria.
* **Variable Objetivo (Target):** `afiliacion_pension` (`Cotiza activamente` [35,2%] vs `No cotiza` [64,8%]).
* **Total observaciones evaluadas:** 12.350 instancias completas.
* **Estrategia de evaluación:** 10-Fold Stratified Cross-Validation (Replicable sampling activo).

### 2.2 Modelos Evaluados y Comparación en `Test and Score`
Evaluados bajo idénticas condiciones en Orange:

| Modelo | AUC | CA (Accuracy) | F1-Score | Precision | Recall | MCC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (100 árboles)** | **0.833** | **0.749 (74,9%)** | **0.743** | **0.742** | **0.749** | **0.432** |
| **Classification Tree (Depth 5)** | 0.831 | 0.743 (74,3%) | 0.738 | 0.737 | 0.743 | 0.420 |
| **Logistic Regression (Ridge L2)** | 0.783 | 0.720 (72,0%) | 0.699 | 0.711 | 0.720 | 0.345 |

**Comparación Estadística de Curvas ROC ($p$-values):**
* Random Forest vs Logistic Regression: $p = 0.956$ (Superioridad estadística categórica del ensamble no lineal).
* Tree vs Logistic Regression: $p = 0.967$ (El árbol binario simple supera holgadamente a la regresión lineal).
* Random Forest vs Tree: $p = 0.335$ vs $0.665$ (Ligera ventaja de Random Forest en estabilidad).

### 2.3 Análisis de Matrices de Confusión
* **Random Forest:** 9.246 aciertos (74,87%). 1.895 falsos negativos. Alta especificidad (84,88% para detectar informales).
* **Classification Tree:** 9.177 aciertos (74,31%). 1.916 falsos negativos.
* **Regresión Logística:** 8.890 aciertos (71,98%). Genera una falla asimétrica crítica con **2.592 falsos negativos**: el modelo lineal no logra detectar al 59,6% de los cotizantes reales debido al umbral rígido.

### 2.4 Ranking de Importancia de Variables (`Rank`)
1. `cuenta_con_arl` (Gain Ratio: **0.160**, Gini: 0.082) &rarr; Determinante supremo.
2. `tipo_plataforma` (Gain Ratio: **0.048**, Gini: 0.029) &rarr; Segmentación física vs nube.
3. `ingreso_neto_hora_usd` (Gain Ratio: 0.028, Gini: 0.035).
4. `ingreso_neto_mensual_cop` (Gain Ratio: 0.025, Gini: 0.031).
5. `nivel_territorial` (Gain Ratio: 0.023, Gini: 0.023).

---

## 3. Sección 2 · Clustering No Supervisado de Vulnerabilidad

### 3.1 Tratamiento y Parámetros
* **Algoritmo:** k-Means con $k=3$ y distancia euclídea.
* **Preprocesamiento:** Normalización Z-score ($\mu=0, \sigma=1$) sobre 8 variables métricas laborales.
* **Calidad de Agrupamiento:** Coeficiente medio positivo de Silhouette (~0.12) sin ramas fuertemente negativas.

### 3.2 Caracterización de los Tres Clusters
* **Cluster C1 ("Núcleo de Precarización Física"):** 72,0% No cotiza a pensión y solo 28,0% cotiza. Representa el trabajo físico en reparto y transporte con sobrecarga de horas (&gt; 52 h/sem) y tarifas bajas (&lt; 3 USD/h).
* **Cluster C2 ("Freelancers en la Nube"):** 49,0% Cotiza y 51,0% No cotiza. Trabajo profesional remoto calificado con tarifas altas (12–25 USD/h).
* **Cluster C3 ("Trabajadores Mixtos y de Transición"):** 50,0% Cotiza y 50,0% No cotiza. Jornadas variables e ingresos complementarios de emergencia.

**Validación Estadística Externa (Box Plot):**
Prueba Chi-cuadrado entre los clusters y la cotización a pensión:
$$\chi^2 = 553,07 \quad (p = 0,000, \text{ dof} = 2)$$
Rechazo rotundo de independencia: el clustering agrupa intrínsecamente la precariedad sin haber conocido la variable target.

---

## 4. Sección 3 · Minería de Texto en Comentarios de YouTube

### 4.1 Extracción y Limpieza
* **Fuente:** YouTube Data API v3 (Video: `OXT8xdqcAoU`, debate documental sobre Gig Economy).
* **Muestra:** 262 comentarios extraídos &rarr; 242 documentos depurados tras remoción de URLs, signos especiales y stopwords bilingües.
* **Tokens totales:** 1.027 palabras procesadas.

### 4.2 Modelado de Tópicos LDA (7 Tópicos)
* **Log-perplejidad:** `31.53162`
* **Topic Coherence:** `0.40812`
* **Ejes descubiertos:**
  * **Tópico 1:** Salud y desprotección física (`gig, economy, freelance, health, work`).
  * **Tópico 3:** Monetización y captación de clientes (`good, freelancing, clients, money`).
  * **Tópico 6:** Degradación de tarifas salariales (`like, work, pay, better, market`).

### 4.3 Evidencia Cualitativa en Corpus Viewer
Comentario con mayor impacto (539 likes, Cluster C3):
> *"It's as you said Ted Ed, freelancing is definitely a good support net for quick money. It's safe for part timers, but maybe not in the long run."*

---

## 5. Catálogo de Conocimientos Ocultos Descubiertos

### KO-1.1 — La ARL como Condicionante No Lineal de la Cotización Pensional
* **Pregunta:** ¿Qué variables determinan la formalidad pensional en la economía de plataformas?
* **Hallazgo:** La cobertura de ARL multiplica exponencialmente la cotización (Gain Ratio 0.160). La regla de decisión en el árbol demuestra que tener ARL en escala Nacional/Regional genera 100% de cotización (941/941). Quien carece de ARL cae en un 92,8% de no cotización en trabajo físico.
* **Interpretación:** Formalidad "en bloque": no existe cotización parcial; el trabajador entra al esquema completo o queda en la desprotección absoluta.

### KO-1.2 — Superioridad de Ensamble y Falla Asimétrica de Modelos Lineales
* **Pregunta:** ¿Responde la formalidad a relaciones lineales aditivas?
* **Hallazgo:** Random Forest (AUC 0.833) supera con $p=0.956$ a la Regresión Logística (AUC 0.783). El modelo lineal genera 2.592 falsos negativos, ignorando al 59,6% de los cotizantes reales.
* **Interpretación:** La transición formal en plataformas opera mediante saltos discretos e interactivos entre costos fijos, tipo de app y formación.

### KO-2.1 — Segmentación Tripartita: El Cluster C1 como Trampa de Subsistencia
* **Pregunta:** ¿Emergen grupos naturales según métricas de dedicación e ingreso?
* **Hallazgo:** k-Means aísla el Cluster C1 con un 72,0% de exclusión pensional ($\chi^2 = 553,07, p = 0,000$).
* **Interpretación:** La desprotección no es una decisión voluntaria aislada, sino una consecuencia estructural del perfil físico de subsistencia.

### KO-2.2 — Divergencia Bivariada: Ineficacia de la Sobrecarga Horaria
* **Pregunta:** ¿Trabajar más horas incrementa la probabilidad de afiliación formal?
* **Hallazgo:** En el Scatter Plot, los no cotizantes se apilan densamente en una columna vertical a baja tarifa (&lt; 2 desviaciones) abarcando de 10 a 70 h/semana.
* **Interpretación:** El trabajador atrapado en plataformas físicas aumenta sus horas para cubrir gastos operativos, sin generar excedente para cotizar.

### KO-3.1 — Disonancia Temporal: Red de Liquidez Rápida vs Ruina Futura
* **Pregunta:** ¿Cómo perciben los trabajadores la sostenibilidad temporal de la Gig Economy?
* **Hallazgo:** El análisis textual identifica que los trabajadores reconocen la app como un mecanismo de liquidez de corto plazo, pero admiten su inviabilidad en el largo plazo por falta de jubilación.
* **Interpretación:** Contradice la narrativa de "libertad laboral"; el discurso revela resignación ante la urgencia económica diaria.

### KO-3.2 — Convergencia Léxica: Salud y Seguros como Núcleo de la Demanda Social
* **Pregunta:** ¿Coincide el vocabulario espontáneo con las variables matemáticas predictoras?
* **Hallazgo:** Términos como `health` y `insurance` dominan la nube de palabras y el Tópico 1, triangulando con el resultado donde `cuenta_con_arl` lidera el ranking de características.
* **Interpretación:** Validez convergente: la prioridad que el modelo matemático descubre es idéntica a la carencia que los trabajadores expresan humanamente.

---

## 6. Decisiones Reguladoras Sustentadas
1. **Afiliación automática a ARL a cargo de las aplicaciones:** Al ser el disparador del árbol, resolver el aseguramiento en riesgos laborales desbloquea la formalización.
2. **Micro-aportes pensionales obligatorios por servicio completado:** Para rescatar al 72% del Cluster C1 atrapado en la trampa de horas.
3. **Desconexión algorítmica obligatoria tras 8 horas de conexión:** Para frenar la autoexplotación inútil evidenciada en el Scatter Plot.
4. **Programas de reconversión hacia habilidades digitales:** Facilitar la migración de repartidores y conductores hacia el Cluster C2 en la nube.
