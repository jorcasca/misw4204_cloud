from flask_sqlalchemy import SQLAlchemy

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

class Ruta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    
class RutaSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Ruta
         include_relationships = True
         load_instance = True
         
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100)) 
    email = db.Column(db.String(100), unique=True)
    
class Tareas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timeStamp = db.Column(db.String(50))
    fileName = db.Column(db.String(500))
    newFormat = db.Column(db.String(100))
    status = db.Column(db.String(50)) # uploaded/processed
    usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class TareasSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tareas
        include_relationships = True
        load_instance = True
        
    id = fields.String()
    timeStamp = fields.String()
    fileName = fields.String()
    newFormat = fields.String()
    status = fields.String() # uploaded/processed
    usuario = fields.String()

