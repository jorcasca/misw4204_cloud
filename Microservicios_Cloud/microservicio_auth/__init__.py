from flask import Flask
from modelos import db

def create_app(config_name):
    app = Flask(__name__)  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:contrasena123@<POSTGRES_SERVER_IP>/baseapp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app_context = app.app_context()
    app_context.push()
    db.init_app(app)
    return app
