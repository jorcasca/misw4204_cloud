from microservicio_worker import create_app
from flask_restful import Api
from .vistas import VistaTask
from .modelos import db

app = create_app('default')
db.create_all()

api = Api(app)
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')
