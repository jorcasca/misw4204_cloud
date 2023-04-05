from flask_restful import Resource
from ..modelos import Ruta, RutaSchema, Usuario, db, Tareas, TareasSchema
from flask_jwt_extended import jwt_required, create_access_token
from flask import request

ruta_schema = RutaSchema()
tareas_schema = TareasSchema()


class VistaRuta(Resource):
    def get(self):
        return [ruta_schema.dump(ruta) for ruta in Ruta.query.all()]
        
class VistaAuthSignup(Resource):
    def post(self):
        usuario = Usuario.query.filter(Usuario.username == request.json["username"]).first()
        if  (request.json["password1"] != request.json["password2"]):
            return "El password ingresado No coincide", 404
        elif usuario is not None:
            return "El usuario {} ya existe".format(request.json["username"]), 404
        else:
            email = Usuario.query.filter(Usuario.email == request.json["email"]).first()
            if email is not None:
                return "El correo ingresado {} ya existe".format(request.json["email"]), 404
            else:
                nuevo_usuario = Usuario(username = request.json["username"],
                                        password = request.json["password1"],
                                        email = request.json["email"]
                                        ) 
                db.session.add(nuevo_usuario)
                db.session.commit()
                return "Se creo el usuario satisfactoriamente."
            
            
class VistaLogin(Resource):
    def post(self):
        #contrasena_encriptada = hashlib.md5(request.json["contrasena"].encode('utf-8')).hexdigest()
        usuario = Usuario.query.filter(Usuario.username == request.json["username"],
                                       Usuario.password == request.json["password"]).first()
        db.session.commit()
        if usuario is None:
            return "Usuario o password Incorrectos", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id, "username": usuario.username}
        
        
class VistaTasks(Resource):
    
    @jwt_required()
    def get(self):
        
        if (request.json["max"] is None):
            if (int(request.json["order"]) == 0):
                tasks = Tareas.query.order_by(Tareas.id.desc()).all()
            elif (int(request.json["order"]) == 1):
                tasks = Tareas.query.order_by(Tareas.id.asc()).all()
            else:
                tasks = Tareas.query.order_by(Tareas.id.asc()).all()
        else:
            if (int(request.json["max"]) > 0) & (int(request.json["order"]) == 0):
                tasks = Tareas.query.order_by(Tareas.id.desc()).limit(int(request.json["max"]))
            elif (int(request.json["max"]) > 0) & (int(request.json["order"]) == 1):
                tasks = Tareas.query.limit(int(request.json["max"]))
            else:
                tasks = Tareas.query.order_by(Tareas.id.asc()).all()
            
        return [tareas_schema.dump(tarea) for tarea in tasks]


       