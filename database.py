""" from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

URI_DB = 'postgresql+psycopg2://postgres:SIGEA_DB@localhost:5432/gig_economy_db'
# URI_DB = 'postgresql+psycopg2://postgres:tu_contraseña@localhost:5432/gig_economy_db'


def init_db(app):
    db.init_app(app) """
    
    
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL no configurada")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True
    }

    db.init_app(app)