import os
from flask import Flask, render_template, request, jsonify, send_file
import data_service

app = Flask(__name__)

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


@app.route('/descargar-dataset')
def descargar_dataset():
    data_service.ensure_dataset_exists()
    return send_file(
        data_service.CSV_PATH,
        as_attachment=True,
        download_name='dataset_gig_economy_consolidado.csv',
        mimetype='text/csv'
    )


@app.route('/api/dataset')
def api_dataset():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '', type=str)
    nivel = request.args.get('nivel', '', type=str)
    tipo_plat = request.args.get('tipo', '', type=str)
    pais = request.args.get('pais', '', type=str)
    
    pagination = data_service.get_filtered_sample(
        page=page, per_page=12, search=search, nivel=nivel, tipo_plat=tipo_plat, pais=pais
    )
    return jsonify(pagination)


if __name__ == '__main__':
    app.run(debug=True)
