# Etapa 1 - Formulación y contextualización del problema de investigación

## Objetivo

Formular y contextualizar un problema de investigación a partir del tema asignado, identificando las preguntas que orientarán el proceso de minería de datos, las necesidades de información, las fuentes disponibles y las características iniciales del conjunto de datos.

La actividad busca que cada grupo construya una base sólida antes de aplicar técnicas de minería de datos, comprendiendo primero qué se quiere descubrir, qué datos son necesarios y de dónde provienen.

El análisis debe contemplar los niveles:

* Global.
* Nacional: Colombia.
* Regional.

Las fuentes deben ser:

* Primarias.
* Secundarias.
* Terciarias.

---

# Instrucciones

Cada grupo deberá desarrollar una **aplicación web en Flask** que funcionará como bitácora técnica y plataforma de documentación de todo el proyecto de Minería de Datos.

A partir de este primer entregable, la aplicación deberá mantenerse y evolucionar durante las siguientes etapas del proyecto.

---

## 1. Definición del problema

A partir del tema Mercado laboral y transformacion del empleo, el grupo deberá:

* Describir el contexto general del tema.
* Delimitar un problema específico de investigación.
* Analizar el fenómeno desde tres niveles:

  * Global.
  * Nacional: Colombia.
  * Regional.
* Formular una pregunta principal de investigación.
* Formular mínimo tres preguntas secundarias.
* Explicar qué conocimiento espera obtener a partir de los datos.

Las preguntas deben poder ser respondidas mediante evidencia disponible en los datos y deben orientar:

* Variables.
* Periodos.
* Poblaciones.
* Relaciones.
* Patrones.

Estos elementos serán posteriormente analizados mediante técnicas de minería de datos.

---

## 2. Necesidades de información

El grupo deberá determinar qué información necesita para responder las preguntas planteadas.

Debe identificar como mínimo:

* Entidades involucradas.
* Variables relevantes.
* Periodo de análisis.
* Cobertura geográfica.
* Población o unidad de análisis.
* Nivel de granularidad requerido.
* Variables que permitan comparar las escalas global, nacional y regional.

Cada variable incluida deberá tener una razón clara para formar parte del análisis.

---

## 3. Recolección y selección de fuentes

El grupo deberá identificar y documentar las fuentes utilizadas.

Se deberán utilizar como mínimo **dos fuentes de información por cada nivel**.

### Tipos de fuentes

#### Fuentes primarias

Información obtenida directamente mediante:

* Encuestas.
* Entrevistas.
* Observación.
* Sensores.
* Experimentos.
* Otros mecanismos de recolección directa.

#### Fuentes secundarias

Datos previamente recolectados por:

* Entidades públicas.
* Organizaciones.
* Empresas.
* Repositorios.
* Investigaciones.

#### Fuentes terciarias

Fuentes que integran o distribuyen datos recopilados por terceros.

### Información requerida por fuente

Para cada fuente deberán documentarse:

* Nombre de la fuente.
* Institución responsable.
* URL.
* Tipo de fuente.
* Cobertura geográfica.
* Periodo disponible.
* Formato.
* Método de adquisición.
* Número aproximado de registros.
* Variables disponibles.
* Fecha de consulta o descarga.
* Restricciones o condiciones de uso.

Además, se deberá justificar:

* Pertinencia.
* Confiabilidad.
* Actualidad.
* Cobertura.

---

## 4. Construcción del dataset inicial

El ecosistema inicial de datos deberá cumplir como mínimo con:

* **10.000 registros consolidados.**
* **Mínimo 10 variables.**
* **Mínimo 3 variables numéricas.**
* **Mínimo 3 variables categóricas.**
* **Mínimo 1 variable temporal.**
* **Mínimo 1 variable geográfica.**
* Información suficiente para trabajar los niveles global, nacional y regional.
* Posibilidad de integrar las fuentes mediante variables geográficas, temporales o ambas.

Se deberá priorizar el uso de datos con suficiente granularidad y evitar trabajar únicamente con datos excesivamente agregados.

---

## 5. Caracterización de los datos

El grupo deberá identificar y documentar:

* Unidad de análisis.
* Registro.
* Variables.
* Tipo de cada variable.
* Unidad de medida cuando corresponda.
* Dominio o posibles valores.

Se deberá elaborar un **diccionario de datos** que permita comprender el conjunto de datos sin depender de explicaciones verbales del grupo.

---

## 6. Diagnóstico inicial de calidad

En esta etapa no se realizará todavía la limpieza completa del dataset.

El objetivo será diagnosticar su estado inicial.

Se deberá identificar:

* Valores faltantes.
* Registros duplicados.
* Inconsistencias.
* Valores fuera de los dominios esperados.
* Diferencias de formato.
* Problemas de integración entre fuentes.
* Posibles sesgos.
* Limitaciones del dataset.

El grupo deberá garantizar la **trazabilidad de los datos**, conservando las fuentes originales y documentando las transformaciones o filtros utilizados durante la adquisición.

---

# Desarrollo en GitHub

Todo el desarrollo correspondiente a esta actividad deberá realizarse utilizando control de versiones con **Git y GitHub**.

Cada grupo deberá trabajar el entregable completo en una rama específica para la Etapa 1.

### Nombre sugerido

```text
feature/etapa-1
```

o

```text
r1-problema-datos
```

---

## Flujo de trabajo obligatorio

1. Crear la rama correspondiente a la Etapa 1 a partir de la rama principal.
2. Todo el código, documentación, plantillas, recursos y ajustes de esta entrega deberán desarrollarse dentro de dicha rama.
3. Los integrantes deberán realizar commits identificables y coherentes con los cambios realizados.
4. No se deberá desarrollar directamente sobre la rama principal.
5. Una vez finalizada y validada la actividad, la rama deberá ser integrada a la rama principal mediante `merge`.
6. La versión publicada deberá corresponder a la versión integrada en la rama principal.

Se evaluará que exista evidencia del trabajo colaborativo del grupo a través del historial de commits.

---

# Estructura obligatoria de la aplicación Flask

La aplicación deberá incluir un menú principal llamado:

## Etapa 1

Dentro de este menú deberá existir un submenú con los siguientes elementos:

1. **Problema y contexto**
2. **Pregunta principal y preguntas secundarias**
3. **Necesidades de información**
4. Necesidades de información
5. **Dataset**
6. **Diccionario de datos**
7. **Calidad inicial de los datos**
8. **Limitaciones y consideraciones**

Cada submenú deberá mostrar información suficiente para comprender el trabajo realizado sin necesidad de una explicación oral adicional.

Este principio está alineado con la estructura planteada para la página del primer entregable.

---

# Formato de entrega

La entrega se realizará mediante un documento o formulario de entrega que contenga **únicamente la información necesaria para acceder y verificar el proyecto**.

Debe incluir:

### Información del proyecto

**Nombre del proyecto:**

**Tema asignado:**

**Integrantes:**

* Integrante 1
* Integrante 2
* Integrante 3
* Integrante 4

**Repositorio GitHub:**

```text
https://github.com/...
```

**Rama utilizada para el desarrollo de la Etapa 1:**

```text
feature/etapa-1
```

**URL de la aplicación Flask publicada:**

```text
https://...
```

La URL publicada deberá permitir acceder directamente a la aplicación funcional.

---

## No se considerará completa la entrega si:

* El repositorio no es accesible.
* La aplicación no está publicada.
* La Etapa 1 no se encuentra integrada en la rama principal.
* Los enlaces entregados no funcionan.
* La información requerida no se encuentra documentada dentro de Flask.

---

# Criterios de evaluación

| Criterio                                                        | Descripción                                                                                                                                                                                                            |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Formulación y contextualización del problema**             | Claridad, pertinencia y delimitación del problema. Articulación del análisis en escala global, nacional y regional. Coherencia entre el tema, la pregunta principal y las preguntas secundarias.                       |
| **2. Identificación y justificación de fuentes de información** | Calidad, confiabilidad, actualidad, cobertura y pertinencia de las fuentes. Correcta clasificación de las fuentes y justificación de su utilidad para responder el problema planteado.                                 |
| **3. Caracterización del dataset y calidad de los datos**       | Cumplimiento de los requisitos mínimos de registros y variables, identificación de unidad de análisis, tipos de variables, cobertura geográfica y temporal, granularidad y diagnóstico inicial de calidad.             |
| **4. Diccionario de datos y trazabilidad**                      | Claridad y completitud del diccionario de datos, identificación de procedencia, significado, tipo, unidad, dominio, restricciones y capacidad de rastrear el origen de los datos utilizados.                           |
| **5. Coherencia analítica y potencial para Minería de Datos**   | Correspondencia entre problema, preguntas, variables y fuentes. Posibilidad real de continuar posteriormente con análisis multidimensional, asociación, clustering, predicción y comparación global–nacional–regional. |

---

# Restricciones

GitHub, uso de la rama correspondiente, integración a la rama principal, publicación de la aplicación Flask, funcionamiento de la URL y estructura obligatoria de menús son **requisitos mínimos de entrega**.

Estos requisitos **no otorgan puntos adicionales**; su incumplimiento genera descuentos sobre la calificación obtenida.
