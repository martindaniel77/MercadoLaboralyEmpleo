## Especificaciones para correr el proyecto en local

1. Tener python instalado
2. git clone al repositorio https://github.com/martindaniel77/MercadoLaboralyEmpleo.git
`git clone https://github.com/martindaniel77/MercadoLaboralyEmpleo.git`
3. Establecer el entorno virtual la manera mas sencilla es:

~~~~
    # cntrl + shift + p - escribir python:Create enviroment

    # Una vez configurado el entorno virtual, crear una nueva terminal
    # la terminal automaticamente estara corriendo en el entorno virtual, debe aparecer al inico de la linea de comando (.venv)
    # si no aparece, ejecutar .venv\Scripts\activate

    # ejecutar en la terminal
    pip install -r requirements.txt

    # Si no funciona probar con este comando 
    py -m pip install -r requirements.txt

    # Correr el servicio, en terminal ejecutar
    flask run
~~~~