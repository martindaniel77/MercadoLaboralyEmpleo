import os
from flask import Flask, render_template, request, jsonify, send_file
import data_service

app = Flask(__name__)

# Configuración del video de la Etapa 3.
# Cuando tengas el enlace del video (YouTube/Drive/MP4), pégalo aquí y la
# sección "Video demostrativo" lo embebe automáticamente. Ejemplos:
#   ETAPA3_VIDEO_URL = "https://www.youtube.com/watch?v=XXXXXXXXXXX"
#   ETAPA3_VIDEO_URL = "https://drive.google.com/file/d/FILE_ID/view"
#   ETAPA3_VIDEO_URL = "/static/videos/demo_etapa3.mp4"
ETAPA3_VIDEO_URL = os.environ.get('ETAPA3_VIDEO_URL', 'https://youtu.be/KBkUWh_jC9U')

# Asegurar que el dataset inicial exista al arrancar
data_service.ensure_dataset_exists()

@app.route('/')
def home():
    summary = data_service.get_dataset_summary()
    return render_template('index.html', summary=summary)


@app.route('/etapa-1/problema')
def problema():
    return render_template('problema.html')


@app.route('/etapa-1/preguntas')
def preguntas():
    return render_template('preguntas.html')


@app.route('/etapa-1/necesidades')
def necesidades():
    diccionario = data_service.DICCIONARIO_DATOS
    return render_template('necesidades.html', variables=diccionario)


@app.route('/etapa-1/fuentes')
def fuentes():
    fuentes_info = data_service.FUENTES_METADATA
    return render_template('fuentes.html', fuentes=fuentes_info)


@app.route('/etapa-1/dataset')
def dataset():
    summary = data_service.get_dataset_summary()
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '', type=str)
    nivel = request.args.get('nivel', '', type=str)
    tipo_plat = request.args.get('tipo', '', type=str)
    pais = request.args.get('pais', '', type=str)
    
    pagination = data_service.get_filtered_sample(
        page=page, per_page=12, search=search, nivel=nivel, tipo_plat=tipo_plat, pais=pais
    )
    
    return render_template(
        'dataset.html',
        summary=summary,
        pagination=pagination,
        search=search,
        nivel=nivel,
        tipo_plat=tipo_plat,
        pais=pais
    )


@app.route('/etapa-1/diccionario')
def diccionario():
    diccionario_datos = data_service.DICCIONARIO_DATOS
    return render_template('diccionario.html', diccionario=diccionario_datos)


@app.route('/etapa-1/calidad')
def calidad():
    summary = data_service.get_dataset_summary()
    diccionario_datos = data_service.DICCIONARIO_DATOS
    return render_template('calidad.html', summary=summary, diccionario=diccionario_datos)


@app.route('/etapa-1/limitaciones')
def limitaciones():
    return render_template('limitaciones.html')


# ============================================================
# RUTAS DE LA ETAPA 2: CALIDAD, DIAGNÓSTICO Y TRATAMIENTO
# ============================================================

@app.route('/etapa-2/proposito-requisitos')
def etapa2_proposito():
    requisitos = data_service.REQUISITOS_CALIDAD
    return render_template('etapa2_proposito.html', requisitos=requisitos)


@app.route('/etapa-2/perfilamiento')
def etapa2_perfilamiento():
    profile = data_service.profile_dataset('raw')
    diccionario_datos = data_service.DICCIONARIO_DATOS
    return render_template('etapa2_perfilamiento.html', profile=profile, diccionario=diccionario_datos)


@app.route('/etapa-2/dimensiones-metricas')
def etapa2_dimensiones():
    dimensions = data_service.calculate_quality_dimensions('raw')
    return render_template('etapa2_dimensiones.html', dimensions=dimensions)


@app.route('/etapa-2/inventario-problemas')
def etapa2_inventario():
    inventory = data_service.get_problem_inventory()
    causes = data_service.get_root_cause_analysis()
    auditoria = data_service.get_variable_audit()
    return render_template('etapa2_inventario.html', inventory=inventory, causes=causes, auditoria=auditoria)


@app.route('/etapa-2/plan-tratamiento')
def etapa2_tratamiento():
    steps = data_service.get_treatment_plan_steps()
    ssis_info = data_service.get_ssis_package_info()
    return render_template('etapa2_tratamiento.html', steps=steps, ssis=ssis_info)



@app.route('/descargar-dataset')
def descargar_dataset():
    data_service.ensure_dataset_exists()
    return send_file(
        data_service.CSV_PATH,
        as_attachment=True,
        download_name='dataset_gig_economy_inicial_raw.csv',
        mimetype='text/csv'
    )


@app.route('/descargar-dataset-tratado')
def descargar_dataset_tratado():
    return send_file(
        data_service.CSV_TRATADO_PATH,
        as_attachment=True,
        download_name='dataset_gig_economy_tratado_limpio.csv',
        mimetype='text/csv'
    )


# ============================================================
# RUTAS DE LA ETAPA 3: ETL CON SSIS - TRATAMIENTO Y VIDEO
# ============================================================

@app.route('/etapa-3/reglas-tratamiento')
def etapa3_reglas():
    reglas = data_service.get_etapa3_reglas()
    return render_template('etapa3_reglas.html', reglas=reglas)


@app.route('/etapa-3/arquitectura-ssis')
def etapa3_arquitectura():
    arch = data_service.get_etapa3_arquitectura()
    return render_template('etapa3_arquitectura.html', arch=arch)


@app.route('/etapa-3/iteraciones')
def etapa3_iteraciones():
    data = data_service.get_etapa3_iteraciones()
    return render_template('etapa3_iteraciones.html', data=data)


@app.route('/etapa-3/comparacion-calidad')
def etapa3_comparacion():
    data = data_service.get_etapa3_comparacion()
    return render_template('etapa3_comparacion.html', data=data)


@app.route('/etapa-3/video-demostrativo')
def etapa3_video():
    return render_template('etapa3_video.html', video_url=ETAPA3_VIDEO_URL)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


if __name__ == '__main__':
    app.run(debug=True)

