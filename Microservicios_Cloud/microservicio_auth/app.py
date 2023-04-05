from microservicio_auth import create_app
from flask_restful import Api
from .vistas import VistaAuthSignup, VistaLogin, VistaTasks, VistaTask
from .modelos import db
from flask_jwt_extended import JWTManager


app = create_app('default')
app_context = app.app_context()
app_context.push()

app.config['JWT_SECRET_KEY'] = 'frase-secreta'

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaAuthSignup, '/api/auth/signup')
api.add_resource(VistaLogin, '/api/auth/login')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')

jwt = JWTManager(app)