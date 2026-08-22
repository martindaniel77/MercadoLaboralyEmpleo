from flask import Flask

app = Flask(__name__)


@app.route('/')
def home ():
    return '<h1> Esta es la pagina principal de la bitacora Mercado Laboral y Empleo </h1>'