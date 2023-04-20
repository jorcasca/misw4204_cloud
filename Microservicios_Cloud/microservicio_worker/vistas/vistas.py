from flask_restful import Resource
from ..tareas import convert_file

class VistaTask(Resource):

    def get(self, id_task):
        convert_file.delay(id_task)
        return {'message': 'la tarea fue creada.'}
