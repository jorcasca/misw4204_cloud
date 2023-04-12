from flask_restful import Resource
from ..modelos import Usuario, db, Tareas, TareasSchema
from ..tareas import convert_file
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask import request, send_file
from sqlalchemy import or_
import hashlib
import os

tareas_schema = TareasSchema()


def validateStrongPassword(password):
    if len(password) < 8:
        return False

    if not any(c.isupper() for c in contrasena):
        return False

    if not any(c.isdigit() for c in contrasena):
        return False

    return True


class VistaAuthSignup(Resource):

    def post(self):
        usuario = Usuario.query.filter(
            Usuario.username == request.json["username"]).first()

        validate_passwd = validateStrongPassword(request.json["password1"])

        if not validate_passwd:
            return "El password ingresado no cumple con los requisitos minimos de seguridad. Debe tener al menos 8 caracteres, debe tener al menos una letra mayúscula, debe tener al menos un número ", 400

        elif (request.json["password1"] != request.json["password2"]):
            return "El password ingresado No coincide", 404
        elif usuario is not None:
            return "El usuario {} ya existe".format(request.json["username"]), 404
        else:
            email = Usuario.query.filter(
                Usuario.email == request.json["email"]).first()
            if email is not None:
                return "El correo ingresado {} ya existe".format(request.json["email"]), 404
            else:
                nuevo_usuario = Usuario(username=request.json["username"],
                                        password=hashlib.md5(
                                            request.json["password1"].encode('utf-8')).hexdigest(),
                                        email=request.json["email"]
                                        )
                db.session.add(nuevo_usuario)
                db.session.commit()
                return "Se creo el usuario satisfactoriamente."


class VistaLogin(Resource):

    def post(self):
        usuario = Usuario.query.filter(
            or_(Usuario.username == request.json.get("username"),
                Usuario.email == request.json.get("username")),
            Usuario.password == request.json.get("password")
        ).first()
        db.session.commit()
        if usuario is None:
            return "Usuario o password Incorrectos", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id, "username": usuario.username}


class VistaTasks(Resource):

    @jwt_required()
    def get(self):
        if (request.json["max"] is not None and request.json["order"] is not None):
            if (int(request.json["order"]) == 0):
                tasks = Tareas.query.order_by(Tareas.id.desc()).all()

            elif (int(request.json["order"]) == 1):
                tasks = Tareas.query.order_by(Tareas.id.asc()).all()

            elif (int(request.json["max"]) > 0) & (int(request.json["order"]) == 0):
                tasks = Tareas.query.order_by(
                    Tareas.id.desc()).limit(int(request.json["max"]))

            elif (int(request.json["max"]) > 0) & (int(request.json["order"]) == 1):
                tasks = Tareas.query.limit(int(request.json["max"]))

        else:
            tasks = Tareas.query.order_by(Tareas.id.asc()).all()

        return [tareas_schema.dump(tarea) for tarea in tasks]

    @jwt_required()
    def post(self):
        file = request.files.get('fileName')
        new_format = request.form.get('newFormat')
        user_id = get_jwt_identity()
        if not os.path.exists('archivos/originales'):
            os.makedirs('archivos/originales')
        file_name = file.filename
        file.save(os.path.join('archivos/originales', file_name))
        nueva_tarea = Tareas(
            fileName=file_name, newFormat=new_format, status='uploaded', usuario=user_id)
        db.session.add(nueva_tarea)
        db.session.commit()
        convert_file.delay(nueva_tarea.id)
        return {'message': 'la tarea fue creada.'}


class VistaTask(Resource):

    @jwt_required()
    def delete(self, id_task):
        tarea = Tareas.query.get_or_404(id_task)
        if tarea.status != 'processed':
            return {'message': 'La tarea no ha sido procesada aún'}, 400
        archivo_original_path = os.path.join(
            'archivos/originales', tarea.fileName)
        archivo_convertido_path = os.path.join(
            'archivos/convertidos', tarea.fileName + '.' + tarea.newFormat.lower())
        if os.path.exists(archivo_original_path):
            os.remove(archivo_original_path)
        if os.path.exists(archivo_convertido_path):
            os.remove(archivo_convertido_path)
        db.session.delete(tarea)
        db.session.commit()
        return {'message': 'Tarea y archivos eliminados correctamente.'}

    @jwt_required()
    def get(self, id_task):
        tarea = Tareas.query.get_or_404(id_task)
        return tareas_schema.dump(tarea)


class VistaFile(Resource):

    @jwt_required()
    def get(self, filename):
        try:
            nombre, extension = os.path.splitext(filename)
            if extension:
                return send_file('archivos/convertidos/'+filename, as_attachment=True)
            else:
                return send_file('archivos/originales/'+filename, as_attachment=True)
        except FileNotFoundError:
            abort(404)
