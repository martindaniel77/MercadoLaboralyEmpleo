from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

URI_DB = 'postgresql+psycopg2://postgres:SIGEA_DB@localhost:5432/gig_economy_db'
# URI_DB = 'postgresql+psycopg2://postgres:tu_contraseña@localhost:5432/gig_economy_db'


def init_db(app):
    db.init_app(app)