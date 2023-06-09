from __init__ import create_app
from flask_restful import Api
from vistas import VistaAuthSignup, VistaLogin, VistaTasks, VistaTask, VistaFile
from flask_jwt_extended import JWTManager
from modelos import db

app = create_app('default')
db.create_all()

api = Api(app)
api.add_resource(VistaAuthSignup, '/api/auth/signup')
api.add_resource(VistaLogin, '/api/auth/login')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')
api.add_resource(VistaFile, '/api/files/<string:filename>')

jwt = JWTManager(app)
