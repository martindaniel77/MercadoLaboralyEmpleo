from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/etapa-1/problema')
def problema():
    return render_template('problema.html')


@app.route('/etapa-1/preguntas')
def preguntas():
    return render_template('preguntas.html')


@app.route('/etapa-1/necesidades')
def necesidades():
    return render_template('necesidades.html')


@app.route('/etapa-1/fuentes')
def fuentes():
    return render_template('fuentes.html')


@app.route('/etapa-1/dataset')
def dataset():
    return render_template('dataset.html')


@app.route('/etapa-1/diccionario')
def diccionario():
    return render_template('diccionario.html')


@app.route('/etapa-1/calidad')
def calidad():
    return render_template('calidad.html')


@app.route('/etapa-1/limitaciones')
def limitaciones():
    return render_template('limitaciones.html')


if __name__ == '__main__':
    app.run(debug=True)
