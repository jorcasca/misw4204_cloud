from flask import Flask
from .modelos import db

def create_app(config_name):
    app = Flask(__name__)  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'spostgresql://postgres:contrasena123@localhost/baseapp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app_context = app.app_context()
    app_context.push()
    db.init_app(app)
    return app