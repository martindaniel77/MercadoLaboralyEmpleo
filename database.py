from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

URI_DB = 'postgresql://postgres:Contrasenia@localhost:5432/gig_economy_db'

def init_db(app):
    db.init_app(app)