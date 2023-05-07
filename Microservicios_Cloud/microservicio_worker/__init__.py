from flask import Flask
from .modelos import db
import os

def create_app(config_name):
    app = Flask(__name__)  
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/jorcasca/misw4204_cloud/Microservicios_Cloud/microservicio_worker/credentials.json"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:contrasena123@localhost/baseapp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app_context = app.app_context()
    app_context.push()
    db.init_app(app)
    return app
