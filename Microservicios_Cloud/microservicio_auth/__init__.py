from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app(config_name):
    app = Flask(__name__)  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///archivos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    return app